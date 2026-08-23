#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge a directory harvest into harvest/resources.json, under a gate.

WHY THIS EXISTS. 78% of the unlinked rows in resources.json sit in categories
where one authoritative directory covers every country. Looking them up one
search at a time closes about two rows a round; a directory closes a hundred in
one run. `bch_focal_points.py` has read the Secretariat's own focal-point list
since it was written and has never been pointed at resources.json.

WHAT IT WILL NOT DO, which matters more than what it will:

  - It never overwrites a `u` that is already there. A hand-verified link
    outranks a harvested one, always.
  - It never renames a row that names a real body. A harvested institution name
    replacing a typed one would be a downgrade dressed as an update.
  - It does not treat the focal point as the regulator. The BCH focal point is
    the office that FILES a country's records under the Cartagena Protocol. In
    many countries that is a different body from the one that decides
    approvals, and the stub text says so. So a focal point is written into a
    `decides` row ONLY where the harvested institution and the row's existing
    name are the same body by the match test below. Where they differ, the row
    is reported for review and left alone.
  - Every row it cannot place is printed. A directory merge that silently drops
    a third of its input looks identical to one that worked.

THE ONE CASE IT FILLS OUTRIGHT. Sixty rows read "No national office identified
- quarantine and plant health" and their descriptions tell the reader to ask
that country's Cartagena focal point. The file has been giving that instruction
without giving an address. Those rows take the focal-point link and their
description names the institution it reaches, with the caveat that it is the
filing office rather than a quarantine desk.

    python3 harvest/merge_directory.py --selftest          # no network, no writes
    python3 harvest/merge_directory.py --dry-run           # report only
    python3 harvest/merge_directory.py                     # apply
"""
import json, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
RESOURCES = HERE / "resources.json"
STUBS = HERE.parent / "bch_stubs.json"
IPPC = HERE / "ippc_contacts.json"

NO_OFFICE = "No national office identified \u2014 quarantine and plant health"

# The focal-point list uses UN long forms; resources.json uses short ones. Every
# name that does not resolve is PRINTED rather than dropped, so this table can
# be grown from the report instead of guessed at up front.
ALIASES = {
    "bolivia (plurinational state of)": "Bolivia",
    "venezuela (bolivarian republic of)": "Venezuela",
    "iran (islamic republic of)": "Iran",
    "viet nam": "Vietnam",
    "republic of korea": "South Korea",
    "democratic people's republic of korea": "North Korea",
    "russian federation": "Russia",
    "syrian arab republic": "Syria",
    "lao people's democratic republic": "Laos",
    "united republic of tanzania": "Tanzania",
    "republic of moldova": "Moldova",
    "brunei darussalam": "Brunei",
    "cabo verde": "Cabo Verde",
    "czechia": "Czech Republic",
    "t\u00fcrkiye": "Turkey",
    "netherlands (kingdom of the)": "Netherlands",
    "united kingdom of great britain and northern ireland": "United Kingdom",
    "united states of america": "United States",
    "micronesia (federated states of)": "Micronesia",
    "c\u00f4te d'ivoire": "C\u00f4te d\u2019Ivoire",
    "democratic republic of the congo": "Democratic Republic of the Congo",
    "state of palestine": "Palestine",
    "eswatini": "Eswatini",
}

_STOP = {"the", "of", "and", "for", "de", "del", "la", "le", "des", "du", "y",
         "national", "ministry", "department", "office", "agency", "authority"}

# REVIEWED BY HAND, so the run stops re-reporting settled cases and a genuinely
# new mismatch is visible instead of buried in nine familiar ones. The reason is
# recorded because the decision is not obvious from the two names alone.
REVIEWED = {
    # Declined: the focal point is a DIFFERENT body from the one the row names,
    # not a longer way of writing it. Linking would send a reader to an office
    # that does not hold what the row promises.
    ("Panama", "Comisión Nacional de Bioseguridad"): "ministry hosts the commission, is not it",
    ("Guatemala", "MAGA — Ministerio de Agricultura"): "directorate sits under environment, not MAGA",
    ("Montenegro", "Ministry of Ecology"): "focal point is a university faculty",
    ("Micronesia", "Department of Environment, Climate Change and Emergency Management"):
        "a different department of government",
    ("San Marino", "Environment Authority"): "focal point is a naturalistic centre",
    # Declined for now: the focal point is a sub-unit INSIDE the body the row
    # names. Same organisation, but the stub URL points at the sub-unit, and a
    # reader sent to a biodiversity desk for a biosafety question has been
    # misdirected inside the right building. Revisit if the stub carries the
    # parent URL.
    ("Lebanon", "Ministry of Environment (Lebanon)"): "sub-unit of the named ministry",
    ("Moldova", "Ministry of Environment (Moldova)"): "sub-unit of the named ministry",
    ("Kuwait", "Environment Public Authority"): "sub-unit of the named authority",
}


def expands_to(short, long_):
    """Is `short` the acronym of `long_`?

    NOT first letters. Spanish and French agency acronyms take SEVERAL letters
    per word: SENASA is SErvicio NAcional SAnidad, so an initials test returns
    SNSEIA and misses it - which is exactly how a run came to hold Honduras for
    review against its own full name. This walks the words in order and lets
    each consume a run of leading letters from the acronym.

    Guarded against coincidence: the acronym must be 4+ letters and must draw
    on at least two words, so a short code cannot swallow a single long word.
    """
    a = re.sub(r"[^A-Za-z]", "", short or "").upper()
    if len(a) < 4:
        return False
    words = [w.upper() for w in re.split(r"[^A-Za-z\u00c0-\u024f]+", long_ or "") if w]
    i, used = 0, 0
    for w in words:
        if i >= len(a):
            break
        n = 0
        while n < len(w) and i < len(a) and w[n] == a[i]:
            n += 1; i += 1
        if n:
            used += 1
    return i == len(a) and used >= 2


def _tokens(name):
    s = re.sub(r"[^a-z0-9\u00c0-\u024f ]", " ", (name or "").lower())
    return {t for t in s.split() if len(t) > 2 and t not in _STOP}


def same_body(row_name, harvested):
    """Are these two strings the same office?

    Deliberately strict. The failure this guards against is writing a Ministry
    of Environment's URL onto a Ministry of Agriculture's row, which reads as a
    working link and is wrong. Requires that the distinctive words of the
    shorter name are almost all present in the longer - "Ministry of
    Environment" matches "Ministry of Environment and Forestry", and does not
    match "Ministry of Agriculture and Rural Development".
    """
    a, b = _tokens(row_name), _tokens(harvested)
    if not a or not b:
        return False
    # An acronym and its expansion are the same body and share no tokens at all.
    # A run held Honduras for review because the row said "SENASA Honduras" and
    # the harvest said "Servicio Nacional de Sanidad e Inocuidad Agroalimentaria",
    # which IS SENASA. Require 4+ letters so short codes cannot collide.
    for short, long_ in ((row_name, harvested), (harvested, row_name)):
        for t in re.split(r"[^A-Za-z]+", short or ""):
            if len(t) >= 4 and t.isupper() and expands_to(t, long_):
                return True
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    return len(short & long_) / len(short) >= 0.75


def load(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def index_stubs(stubs):
    """{resources.json country name: (institution, url)}, plus the unresolved."""
    keyed, unresolved = {}, []
    for s in stubs:
        raw = (s.get("country") or "").strip()
        name = ALIASES.get(raw.lower(), raw)
        inst = re.sub(r"\s*\u2014 BCH national focal point$", "", s.get("name") or "")
        if s.get("url"):
            keyed[name] = (inst, s["url"])
        else:
            unresolved.append(raw)
    return keyed, unresolved


def index_ippc(doc):
    """{resources.json country: designated NPPO name}."""
    keyed = {}
    for rec in (doc or {}).get("contacts", []):
        raw = (rec.get("country") or "").strip()
        name = ALIASES.get(raw.lower(), raw)
        org = (rec.get("organization") or "").strip()
        if org:
            keyed[name] = org
    return keyed


def name_unnamed(doc, ippc):
    """Replace the no-office statement with the office the country designated.

    Sixty rows say no national office was identified. Article VIII.2 of the
    IPPC requires every contracting party to designate an official contact
    point and tell the Secretariat who it is, so for most of these the name is
    not a research question - it is published, by the country itself.

    The row keeps NO URL: the IPPC list has no website column. A named office a
    reader can search for is the improvement here; a link is not on offer. A
    country the IPPC list does not cover keeps the no-office statement, which
    is why that text stays in the file rather than being deleted.
    """
    named, missing = [], []
    for country, cats in doc["countries"].items():
        for rows in cats.values():
            if not isinstance(rows, list):
                continue
            for r in rows:
                if r.get("n") != NO_OFFICE:
                    continue
                org = ippc.get(country)
                if not org:
                    missing.append(country); continue
                r["n"] = org
                r["d"] = (
                    "The office this country has designated as its official contact point "
                    "under Article VIII.2 of the International Plant Protection Convention, "
                    "as published by the IPPC Secretariat. Arriving seed, plant material and "
                    "cargo are inspected here, which is where an organism never approved for "
                    "release would turn up. No website is published in that source, so this "
                    "names the office without linking it. It is a plant health body: it does "
                    "not authorise a release, and it is not the biosafety regulator.")
                named.append((country, org))
    return named, missing


def merge(doc, keyed):
    """Returns (actions, review). Mutates nothing until the caller applies."""
    actions, review, settled = [], [], []
    for country, cats in doc["countries"].items():
        hit = keyed.get(country)
        if not hit:
            continue
        inst, url = hit
        for cat, rows in cats.items():
            if not isinstance(rows, list):
                continue
            for r in rows:
                if r.get("u"):
                    continue                      # never overwrite
                if r.get("n") == NO_OFFICE:
                    actions.append(("focal", country, cat, r, inst, url))
                elif cat == "decides":
                    if same_body(r.get("n", ""), inst):
                        actions.append(("link", country, cat, r, inst, url))
                    elif (country, r.get("n", "")) in REVIEWED:
                        settled.append((country, r.get("n", "")))
                    else:
                        review.append((country, r.get("n", ""), inst, url))
    return actions, review, settled


def apply(actions):
    for kind, country, cat, r, inst, url in actions:
        r["u"] = url
        if kind == "focal":
            r["d"] = (
                "No office has been confirmed by name for this country. The function is "
                "carried out somewhere: arriving seed, plant material and cargo are "
                "inspected, and that is where an organism never approved for release here "
                "would turn up. The link goes to %s, the institution this country has "
                "designated to file its records to the Biosafety Clearing-House under the "
                "Cartagena Protocol. That is the office that will know which desk holds "
                "quarantine; it is not itself a quarantine desk, and it does not take a "
                "complaint about a planting." % inst)


def report(actions, review, unresolved, keyed, doc, settled=()):
    filled = sum(1 for a in actions if a[0] == "focal")
    linked = sum(1 for a in actions if a[0] == "link")
    print("  focal-point address written onto a no-office row : %d" % filled)
    print("  decides row linked, harvested name matches       : %d" % linked)
    print("  decides row held for review, names differ        : %d" % len(review))
    if settled:
        print("  reviewed by hand and declined, not re-listed      : %d" % len(settled))
    print("  stub countries with no URL in the source         : %d" % len(unresolved))
    unmatched = sorted(set(keyed) - set(doc["countries"]))
    print("  stub countries not matching a resources country  : %d" % len(unmatched))
    if unmatched:
        print("      %s" % ", ".join(unmatched[:12]))
        print("      (add to ALIASES; they are printed, never dropped quietly)")
    if review:
        print("\n  HELD FOR REVIEW - harvested body is not the body the row names:")
        for country, rn, inst, url in review[:15]:
            print("      %-20s row: %-34s harvest: %s" % (country[:20], rn[:34], inst[:44]))
        if len(review) > 15:
            print("      ... and %d more" % (len(review) - 15))


def selftest():
    ok = True

    def check(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %-58s %s" % (label, "pass" if good else "FAIL got %r" % (got,)))

    check("same body, one name longer",
          same_body("Ministry of Environment", "Ministry of Environment and Forestry"), True)
    check("different ministries do NOT match",
          same_body("Ministry of Environment", "Ministry of Agriculture and Rural Development"), False)
    check("agriculture vs environment, reversed",
          same_body("Ministry of Agriculture", "Ministry of Environment"), False)
    check("exact match", same_body("Biosafety Council", "Biosafety Council"), True)
    check("empty never matches", same_body("", "Ministry of Environment"), False)
    check("generic-only names do not match on stopwords alone",
          same_body("Ministry of the National Office", "Department of National Agency"), False)

    doc = {"countries": {
        "Guineaville": {
            "complain": [{"n": NO_OFFICE, "lens": "COMPLAINT", "d": "old text"}],
            "decides": [{"n": "Ministry of Environment", "lens": "REGULATOR", "d": "x"}]},
        "Elsewhereia": {
            "decides": [{"n": "Ministry of Agriculture", "lens": "REGULATOR", "d": "x"}]},
        "Alreadyland": {
            "decides": [{"n": "Ministry of Environment", "lens": "REGULATOR",
                         "d": "x", "u": "https://typed.example/"}]},
    }}
    stubs = [
        {"country": "Guineaville", "name": "Ministry of Environment and Forestry \u2014 BCH national focal point",
         "url": "https://env.example/"},
        {"country": "Elsewhereia", "name": "Ministry of Environment \u2014 BCH national focal point",
         "url": "https://other.example/"},
        {"country": "Alreadyland", "name": "Ministry of Environment \u2014 BCH national focal point",
         "url": "https://harvested.example/"},
        {"country": "Nowhereistan", "name": "Ministry of Environment", "url": "https://nope.example/"},
        {"country": "Blankland", "name": "Ministry of Environment", "url": ""},
    ]
    keyed, unresolved = index_stubs(stubs)
    actions, review, settled = merge(doc, keyed)
    apply(actions)

    C = doc["countries"]
    check("no-office row took the focal-point URL",
          C["Guineaville"]["complain"][0]["u"], "https://env.example/")
    check("its description now names the institution",
          "Ministry of Environment and Forestry" in C["Guineaville"]["complain"][0]["d"], True)
    check("matching decides row linked",
          C["Guineaville"]["decides"][0]["u"], "https://env.example/")
    check("MISMATCHED decides row left alone",
          "u" in C["Elsewhereia"]["decides"][0], False)
    check("mismatch reported instead", len(review), 1)
    check("existing hand-typed link NOT overwritten",
          C["Alreadyland"]["decides"][0]["u"], "https://typed.example/")
    check("row names never rewritten",
          C["Guineaville"]["decides"][0]["n"], "Ministry of Environment")
    check("stub with no URL excluded", "Blankland" in keyed, False)
    check("unknown country reported, not merged",
          sorted(set(keyed) - set(C)), ["Nowhereistan"])

    # Acronym matching: a run held Honduras against its own expanded name.
    check("an acronym matches its expansion",
          same_body("SENASA Honduras",
                    "Servicio Nacional de Sanidad e Inocuidad Agroalimentaria"), True)
    check("word-prefix, not initials (initials would give SNSEIA)",
          expands_to("SENASA", "Servicio Nacional de Sanidad e Inocuidad"), True)
    check("a short code cannot swallow one long word",
          expands_to("SERV", "Servicio"), False)
    check("unrelated bodies still refused",
          same_body("Ministry of Ecology", "University of Montenegro, Biotechnical Faculty"), False)
    check("and a different ministry is still refused",
          same_body("MAGA \u2014 Ministerio de Agricultura",
                    "Direcci\u00f3n de Valoraci\u00f3n y Conservaci\u00f3n de la Biodiversidad"), False)

    # Hand-reviewed mismatches stop being re-listed every run.
    doc3 = {"countries": {"Montenegro": {"decides": [
        {"n": "Ministry of Ecology", "lens": "REGULATOR", "d": "x"}]}}}
    k3 = index_stubs([{"country": "Montenegro",
                       "name": "University of Montenegro, Biotechnical Faculty",
                       "url": "https://u.example/"}])[0]
    a3, r3, s3 = merge(doc3, k3)
    check("a reviewed mismatch is settled, not re-reported", (len(r3), len(s3)), (0, 1))
    check("and the row is still left alone", "u" in doc3["countries"]["Montenegro"]["decides"][0], False)

    # The IPPC naming pass.
    doc2 = {"countries": {
        "Guineaville": {"complain": [{"n": NO_OFFICE, "lens": "COMPLAINT", "d": "old"}]},
        "Uncoveredland": {"complain": [{"n": NO_OFFICE, "lens": "COMPLAINT", "d": "old"}]},
    }}
    ippc = index_ippc({"contacts": [
        {"country": "Guineaville", "organization": "Direction de la Protection des V\u00e9g\u00e9taux"},
        {"country": "Blankia", "organization": ""},
    ]})
    named, missing = name_unnamed(doc2, ippc)
    G = doc2["countries"]["Guineaville"]["complain"][0]
    U = doc2["countries"]["Uncoveredland"]["complain"][0]
    check("unnamed row takes the designated office",
          G["n"], "Direction de la Protection des V\u00e9g\u00e9taux")
    check("and is NOT given a link, none is published", "u" in G, False)
    check("its description cites the designation", "Article VIII.2" in G["d"], True)
    check("country the list does not cover keeps the statement", U["n"], NO_OFFICE)
    check("and is reported as missing", missing, ["Uncoveredland"])
    check("empty organization never becomes a name", "Blankia" in ippc, False)

    print("\n%s" % ("all pass" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if not STUBS.exists():
        sys.exit("%s not found. Run harvest/bch_focal_points.py first; it needs "
                 "network the sandbox does not have, so this is a workflow step."
                 % STUBS.name)
    doc = load(RESOURCES)
    # Naming first: a row that gets a name from the IPPC list is no longer the
    # no-office row the BCH pass fills, so the order decides which it takes.
    # Naming wins, because a plant health office named by the country beats a
    # focal point that merely knows who it is.
    if IPPC.exists():
        named, missing = name_unnamed(doc, index_ippc(load(IPPC)))
        print("  unnamed rows given the country's designated NPPO : %d" % len(named))
        print("  countries the IPPC list does not cover           : %d %s"
              % (len(missing), sorted(missing)[:8]))
    else:
        print("  %s absent - run harvest/ippc_contacts.py first; the 60 unnamed "
              "rows keep their statement" % IPPC.name)
    keyed, unresolved = index_stubs(load(STUBS))
    before = sum(1 for cats in doc["countries"].values() for rr in cats.values()
                 if isinstance(rr, list) for r in rr if r.get("u"))
    actions, review, settled = merge(doc, keyed)
    if "--dry-run" not in sys.argv:
        apply(actions)
        RESOURCES.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    report(actions, review, unresolved, keyed, doc, settled)
    after = sum(1 for cats in load(RESOURCES)["countries"].values() for rr in cats.values()
                if isinstance(rr, list) for r in rr if r.get("u"))
    print("\n  linked rows %d -> %d%s" % (before, after,
          "  (dry run, nothing written)" if "--dry-run" in sys.argv else ""))


if __name__ == "__main__":
    main()
