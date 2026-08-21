#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The registry of living modified organisms, and the identifier lookup.

WHY THIS IS NOT A MAP LAYER. An organism has no location. A decision has a
country because a government took it; an organism is a thing, and placing one
would mean inventing a position for every record. So this writes a JSON file
and nothing draws it.

WHAT IT IS FOR. The guides tell a reader to write down the unique identifier,
because it is the one string that follows an engineered organism through every
database on Earth. Nothing on this map could then tell them what MON-877O1-2
actually is. This closes that.

It also repairs a gap in the decisions layer. About a quarter of BCH decision
titles name no organism - they read "Technical Opinion No. 293/2022" - but many
carry the event code. With this file present, a code-only title resolves to its
organism from the same source rather than by inference.

THE GLYPH TRAP, which is the reason everything is compared through a normalised
key. The official identifier writes the letter O as the slashed 0:

    MON-877\u00d81-2      official form
    MON-87701-2      how a decision title usually writes it
    MON 877\u00d81 2      how a spreadsheet sometimes writes it

Three spellings of one code. Comparing them literally finds nothing, and finding
nothing looks exactly like the organism not being in the registry.

    python3 harvest/bch_organisms.py
    python3 harvest/bch_organisms.py --selftest      # no network
"""

import json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "bch_organisms.json"
UA = "GMO-map/1.0 (public research map)"
API = "https://api.cbd.int/api/v2013/index"

NAME_FIELDS = ("title_EN_s", "title_s", "name_EN_s", "name_s")
ORG_FIELDS = ("organismName_EN_s", "organismName_s", "commonName_EN_s",
              "species_EN_s", "species_s", "recipientOrganism_EN_s")
ID_FIELDS = ("uniqueIdentification_s", "uniqueIdentifier_s", "uniqueID_s",
             "oecdUniqueIdentifier_s", "identifier_s")
TRAIT_FIELDS = ("trait_EN_ss", "traits_EN_ss", "modifiedTrait_EN_ss",
                "introducedTrait_EN_ss")
DEV_FIELDS = ("developer_EN_s", "developer_s", "applicant_EN_s", "applicant_s")


def norm(code):
    """One key for every spelling of an identifier.

    Upper-cased, the slashed zero folded to O, and everything that is not a
    letter or a digit removed - which collapses hyphens, spaces and the
    occasional non-breaking space that arrives from a copied table.
    """
    if not code:
        return ""
    s = str(code).upper()
    s = re.sub(r"[^A-Z0-9\u00d8\u00f8]", "", s)
    # The selftest caught the real ambiguity here, and it is the opposite of
    # what the first version assumed. The official form writes the LETTER O as
    # \u00d8; a decision title writes the same position as the DIGIT 0. Folding
    # \u00d8 to O left those two spellings different keys - MON877O12 against
    # MON877012 - which is precisely the failure this function exists to stop.
    #
    # So the ambiguous character class collapses to the digit, not the letter:
    # \u00d8 becomes 0, and a letter O standing next to a digit becomes 0 too.
    # An O inside the maker prefix - MON, DAS, SYN - has no digit beside it and
    # is left alone.
    s = s.replace("\u00d8", "0").replace("\u00f8", "0")
    s = re.sub(r"(?<=[0-9])O", "0", s)
    s = re.sub(r"O(?=[0-9])", "0", s)
    return s


# A code looks like three letters, digits, a check digit: MON-877O1-2. Loose
# enough to catch the spacing variants, tight enough not to match a date.
CODE_RE = re.compile(r"\b([A-Z]{2,4})[\s\-]?([0-9\u00d8O]{3,7})[\s\-]?([0-9])\b")


def find_code(text):
    """The first identifier in a string, or nothing."""
    if not text:
        return None
    m = CODE_RE.search(str(text).upper())
    return "-".join(m.groups()) if m else None


def fetch(url, timeout=60):
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    return urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def query(rows=200, start=0):
    return API + "?" + urlencode({"q": "*:*", "fq": "schema_s:modifiedOrganism",
                                  "rows": rows, "start": start, "wt": "json"})


def docs(body):
    try:
        d = json.loads(body)
    except Exception:
        return [], 0
    r = d.get("response") or d
    return (r.get("docs") or []), int(r.get("numFound") or 0)


def first(doc, names):
    for n in names:
        v = doc.get(n)
        if isinstance(v, list):
            v = v[0] if v else None
        if v not in (None, ""):
            return str(v).strip()
    return ""


def listy(doc, names):
    for n in names:
        v = doc.get(n)
        if isinstance(v, list) and v:
            return [str(x).strip() for x in v if str(x).strip()]
        if v:
            return [str(v).strip()]
    return []


def build(rows):
    """One record per organism, keyed on the normalised identifier."""
    out = {}
    for doc in rows:
        title = first(doc, NAME_FIELDS)
        code = first(doc, ID_FIELDS) or find_code(title)
        if not code:
            continue
        k = norm(code)
        if not k or k in out:
            continue
        out[k] = {
            "id": code,
            "organism": first(doc, ORG_FIELDS) or "",
            "name": title,
            "traits": listy(doc, TRAIT_FIELDS),
            "developer": first(doc, DEV_FIELDS) or "",
        }
    return out


def harvest():
    all_rows, start, total = [], 0, 1
    while start < total:
        try:
            body = fetch(query(start=start))
        except Exception as e:
            print("  stopped at %d (%s)" % (start, str(e)[:50]))
            break
        ds, total = docs(body)
        if not ds:
            break
        all_rows += ds
        start += len(ds)
        print("  %d of %d" % (start, total))
        time.sleep(0.4)

    reg = build(all_rows)
    if not reg:
        print("\nNo organisms parsed. The endpoint answered but the field names "
              "are wrong \u2014 run bch_authorities.py --discover and read what a "
              "modifiedOrganism record actually carries. Guessing at field "
              "names has already cost two rounds on this map.", file=sys.stderr)
        return
    named = sum(1 for v in reg.values() if v["organism"])
    print("\n  %d organisms, %d with a species named" % (len(reg), named))
    OUT.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d"),
                               "note": "Keyed on the normalised identifier: "
                                       "upper case, \u00d8 folded to O, "
                                       "punctuation removed.",
                               "organisms": reg}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print("wrote %s" % OUT.name)


def selftest():
    """No network. The glyph trap is the whole point of this."""
    ok = True

    def check(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %-46s %s" % (label, "pass" if good else
                              "FAIL got %r want %r" % (got, want)))

    check("official glyph normalises", norm("MON-877\u00d81-2"), "MON877012")
    check("plain-O form gives the same key", norm("MON-87701-2"), "MON877012")
    check("spaces give the same key", norm("MON 877\u00d81 2"), "MON877012")
    check("lower case folds", norm("mon-877\u00f81-2"), "MON877012")
    check("empty is empty", norm(""), "")

    check("code found in a title",
          find_code("Technical Opinion on MON-87701-2 soybean"), "MON-87701-2")
    check("no code in a bare title",
          find_code("Technical Opinion No. 293/2022"), None)

    rows = [{"title_EN_s": "MON-877\u00d81-2", "organismName_EN_s": "Glycine max",
             "trait_EN_ss": ["insect resistance"], "developer_EN_s": "Monsanto"},
            {"title_EN_s": "Technical Opinion No. 293/2022"},
            {"title_EN_s": "Soybean MON-87701-2 again"}]
    reg = build(rows)
    check("one record per organism, duplicates folded", len(reg), 1)
    check("keyed on the normalised id", "MON877012" in reg, True)
    check("species carried", reg.get("MON877012", {}).get("organism"), "Glycine max")
    check("untitled row dropped rather than guessed",
          any(v["id"] == "" for v in reg.values()), False)

    print("\n%s" % ("all pass" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    harvest()
