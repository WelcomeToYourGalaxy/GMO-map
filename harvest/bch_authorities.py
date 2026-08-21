#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Competent authorities and focal points from the Biosafety Clearing-House.

WHAT THE LAST RUN SHOWED. bch_decisions.py reached the API and paged it
completely - 3,191 rows, all of them - and then could only use 51, because it
could not find a country on the rest. 154 records had no country field at all
and were parked in the Atlantic. So the endpoint works and the FIELD NAMES are
the problem, and guessing at them from here has already failed once.

This harvester therefore does two things in order:

  1. DISCOVER. It fetches a small sample of each relevant record type and
     prints every field name that appears, with an example value. That output
     is the answer to "which field holds the country", and it costs one run.

  2. HARVEST. Using the field names it found, it writes the competent
     authority and focal point for each country into a shape resources.json
     can merge - one entry per country in the `decides` slot.

It never overwrites a typed entry. resources.json entries written by hand are
checked; these are not, and a harvested name that silently replaced a verified
one would be a downgrade dressed as an update.

    python3 harvest/bch_authorities.py --discover
    python3 harvest/bch_authorities.py
"""

import json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
RES = HERE / "resources.json"
OUT = HERE / "bch_authorities.json"
UA = "GMO-map/1.0 (public research map)"
API = "https://api.cbd.int/api/v2013/index"

# The record types worth asking for. The first two are the target; the rest are
# listed so the discovery pass can show what else is there.
# What the discovery run showed, and why this file now does less than it was
# written to do.
#
# The three schemas it was built around do not exist. What exists is `contact`,
# with 11,150 records - and they are PEOPLE. title_EN_s on a contact is a
# person's name, not an office: the Zimbabwe sample returned an individual and
# their work email address.
#
# Publishing a list of named officials and their addresses is not what this map
# is for, and it is not made acceptable by the source being public. So the
# authority harvest stops here rather than proceeding with what is technically
# available. The competent authorities in resources.json stay hand-written.
#
# The discovery pass is kept, because it is what established this, and because
# it found the field that repairs bch_decisions.py: government_EN_s.
SCHEMAS = [
    "contact",
    "biosafetyLaw",
    "biosafetyDecision",
    "modifiedOrganism",
]

# Field names seen or plausible for country, in preference order. The discovery
# pass exists because this list is a guess and the last one was wrong.
COUNTRY_FIELDS = ["government_s", "government_EN_s", "country_s", "countryName_s",
                  "governmentISO_s", "owner_s", "jurisdiction_s", "government_t"]
NAME_FIELDS = ["title_EN_s", "title_s", "name_EN_s", "name_s", "organization_EN_s",
               "organization_s", "institution_s"]
URL_FIELDS = ["url_s", "website_s", "link_s"]


def fetch(url, timeout=60):
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    return urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def query(schema, rows=50, start=0):
    return API + "?" + urlencode({"q": "*:*", "fq": "schema_s:" + schema,
                                  "rows": rows, "start": start, "wt": "json"})


def docs(body):
    try:
        d = json.loads(body)
    except Exception:
        return [], 0
    r = d.get("response") or d
    return (r.get("docs") or []), int(r.get("numFound") or 0)


def discover():
    """Print the field names. This is the whole point of the first run."""
    for sc in SCHEMAS:
        try:
            body = fetch(query(sc, rows=3))
        except Exception as e:
            print("  %-42s unreachable (%s)" % (sc, str(e)[:40]))
            continue
        ds, n = docs(body)
        print("\n%s \u2014 %d records" % (sc, n))
        if not ds:
            print("  (none)")
            continue
        seen = {}
        for doc in ds:
            for k, v in doc.items():
                if k in seen:
                    continue
                if isinstance(v, list):
                    v = v[0] if v else ""
                s = str(v)
                if 0 < len(s) < 90:
                    seen[k] = s
        for k in sorted(seen):
            print("    %-34s %s" % (k, seen[k][:60]))


def first(doc, names):
    for n in names:
        v = doc.get(n)
        if isinstance(v, list):
            v = v[0] if v else None
        if v not in (None, ""):
            return str(v).strip()
    return ""


def harvest():
    """Focal points only, office and country, no email addresses.

    The first version of this file refused to run at all, on the ground that BCH
    contact records are named individuals. That was an overcorrection. A national
    focal point's details are published BY the Secretariat so that people can
    contact them about biosafety; a map telling somebody to contact their focal
    point is the intended use of that list, not a repurposing of it. They are
    officials in a professional role.

    What is worth avoiding is the side effect: pulling all 11,150 contact records
    would assemble an address book nobody asked for. So this takes focal points
    only, keeps the office and the country, and links to the BCH contact page
    rather than reproducing the address. Same usefulness, no harvested mailing
    list.
    """
    found, start, total = {}, 0, 1
    while start < total:
        try:
            body = fetch(query("contact", rows=200, start=start))
        except Exception as e:
            print("  stopped at %d (%s)" % (start, str(e)[:44])); break
        ds, total = docs(body)
        if not ds:
            break
        for doc in ds:
            # focal points only. The role fields name what the contact IS; a
            # record that does not say is skipped rather than assumed.
            role = " ".join(str(doc.get(k) or "") for k in
                            ("contactType_s", "role_s", "jobTitle_EN_s",
                             "organizationType_s", "type_s")).lower()
            if "focal" not in role:
                continue
            country = first(doc, COUNTRY_FIELDS) or government_prefix(doc)
            office = first(doc, ORG_FIELDS)
            if not country:
                continue
            found.setdefault(country, {
                "office": office or "National biosafety focal point",
                "url": "https://bch.cbd.int/about/contacts",
                "note": "Published by the Cartagena Protocol Secretariat and "
                        "kept current. The contact page holds the current "
                        "officer; this map records the office, not the person."})
        start += len(ds)
        time.sleep(0.4)

    print("  focal points found: %d countries" % len(found))
    if not found:
        print("\nNo focal point records matched. Run --discover and check which "
              "field names the contact's role \u2014 the country field is "
              "government_EN_s or the prefix on grp_government_schema_s.",
              file=sys.stderr)
        return
    OUT.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d"),
                               "note": "Offices and countries only. No email "
                                       "addresses are harvested or written.",
                               "authorities": found}, ensure_ascii=False,
                              indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)
    merge(found)


def government_prefix(doc):
    """The country as an ISO2 code on the front of the grouping field, which is
    how a BCH record carries it when no country field is present."""
    for f in ("grp_government_schema_s", "grp_government_s"):
        v = doc.get(f)
        if isinstance(v, list):
            v = v[0] if v else None
        if v and "_" in str(v):
            code = str(v).split("_", 1)[0].strip()
            if len(code) == 2 and code.isalpha():
                return code.upper()
    return None


ORG_FIELDS = ("organization_EN_s", "organization_s", "institution_EN_s",
              "institution_s", "department_EN_s", "department_s")


def _harvest_disabled():
    found = {}
    for sc in ("biosafetyCompetentNationalAuthority", "biosafetyNationalFocalPoint"):
        start, total = 0, 1
        while start < total:
            try:
                body = fetch(query(sc, rows=200, start=start))
            except Exception as e:
                print("  %s stopped at %d (%s)" % (sc, start, str(e)[:40]))
                break
            ds, total = docs(body)
            if not ds:
                break
            for doc in ds:
                country = first(doc, COUNTRY_FIELDS)
                name = first(doc, NAME_FIELDS)
                if not country or not name:
                    continue
                found.setdefault(country, {"name": name,
                                           "url": first(doc, URL_FIELDS),
                                           "kind": sc})
            start += len(ds)
            time.sleep(0.4)
        print("  %-42s %d countries so far" % (sc, len(found)))

    if not found:
        print("\nNothing usable. Run with --discover and put the real field "
              "names into COUNTRY_FIELDS and NAME_FIELDS at the top of this "
              "file \u2014 the endpoint answers, the names are the problem.",
              file=sys.stderr)
        return

    OUT.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d"),
                               "authorities": found}, ensure_ascii=False,
                              indent=1), encoding="utf-8")
    print("wrote %s: %d countries" % (OUT.name, len(found)))
    merge(found)


def merge(found):
    """Fill the decides slot for countries that have none. Never replaces a
    typed entry: those were checked, these were not."""
    if not RES.exists():
        print("  resources.json not present; nothing merged")
        return
    d = json.loads(RES.read_text(encoding="utf-8"))
    C = d.setdefault("countries", {})
    added = updated = 0
    for country, a in found.items():
        cur = C.setdefault(country, {})
        rows = cur.setdefault("decides", [])
        typed = [r for r in rows if not r.get("conf")]
        if typed:
            continue                        # somebody checked this; leave it
        entry = {"n": (a.get("office") or a.get("name") or "")[:120], "lens": "REGULATOR",
                 "u": a.get("url") or "https://bch.cbd.int/about/contacts",
                 "d": ("The competent national authority notified to the "
                       "Biosafety Clearing-House under the Cartagena Protocol. "
                       "It receives notifications, files the country's decisions "
                       "and is the address for a question about a release."),
                 "src": "BCH"}
        if rows:
            cur["decides"] = [entry]; updated += 1
        else:
            cur["decides"] = [entry]; added += 1
    RES.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("  resources.json: %d countries gained an authority, %d unverified "
          "names replaced with the notified one" % (added, updated))


if __name__ == "__main__":
    if "--discover" in sys.argv:
        discover()
    else:
        harvest()
