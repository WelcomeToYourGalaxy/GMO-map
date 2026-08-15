#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Who owns these places.

Every other harvester here answers "where". This one answers "whose", which is
the question that turns a scatter of dots into a picture of an industry. Fifty
clinics in Brazil is a sector. Fifty clinics in Brazil of which twelve belong to
two companies is a different fact, and nothing on this map could show it.

TWO KINDS OF CLAIM, KEPT APART.

STATED. The register itself names the parent. HFEA prints "Satellite clinic to
Care Fertility London"; CCAC lists five research centres under Agriculture and
Agri-Food Canada; AAALAC gives a member and its parent company; APHIS carries a
legal name and a trading name that differ. These are facts a regulator has
published and they are recorded as such.

INFERRED FROM THE NAME. A chain that trades under one name across a dozen
clinics is visible without any filing: Huntington appears four times in Brazil,
INGENES three times in Mexico, VIDA five. Matching on the name is not the same
as reading a share register - a name can be licensed, sold, or coincidental -
so these are marked as inferred, and the map should say so wherever it shows
them.

WHAT IS NOT HERE. Company filings. Companies House, SEC and ASIC would give the
share registers, the changes of hand and the private-equity owners behind the
trading names, and none of that can be read off a clinic list. This file is the
part that can be built from what the registers already say; it is not a
substitute for that work, and it does not pretend to be a complete picture of
who owns what.

    python3 harvest/ownership.py
    python3 harvest/ownership.py --dry-run
"""

import json, re, sys, time, pathlib
from collections import defaultdict

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "ownership.json"

# The harvest files that carry a parent, and where the parent sits in each.
SOURCES = [
    "hfea_clinics.json", "ccac_redlara.json", "aaalac_facilities.json",
    "aphis_animal_facilities.json", "cdc_art_clinics.json",
    "china_nhc_art.json", "india_nartsr.json", "osm_facilities.json",
]

# Groups that trade under one name across several sites. Matched on the site's
# own name, so the claim is "this place calls itself that", not "this place is
# owned by that". Ordered longest-first so "Care Fertility" is not swallowed by
# a shorter pattern.
GROUPS = [
    "Huntington", "INGENES", "Ingenes", "IVI", "Eugin", "Create Fertility",
    "Care Fertility", "CARE Fertility", "Bourn Hall", "TFP ", "Genesis",
    "GENESIS", "Pranor", "Fertility Associates", "Monash IVF", "Virtus",
    "Nova IVF", "Indira IVF", "Cloudnine", "Apollo", "Fortis", "Manipal",
    "Vida", "VIDA", "Citmer", "CITMER", "Origen", "Concebir", "Procrear",
    "Fertilab", "FERTILAB", "REDLARA", "Charles River", "Envigo", "Inotiv",
    "Jackson Laboratory", "Taconic", "Janvier", "WuXi",
]
GROUP_RE = [(g, re.compile(r"(?<![A-Za-z])" + re.escape(g), re.I))
            for g in sorted(set(GROUPS), key=len, reverse=True)]

# Phrases a register uses to name a parent, stripped so the parent's own name is
# what gets recorded.
LEAD = re.compile(r"^\s*(?:satellite clinic to|a site of|part of|subsidiary of|"
                  r"a member of|division of|owned by)\s*", re.I)


def load(name):
    p = HERE / name
    if not p.exists():
        return []
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print("  ! %s unreadable (%s)" % (name, e), file=sys.stderr)
        return []
    return d.get("projects", [])


def stated_parent(rec):
    """The parent as the register gives it, or nothing."""
    v = str(rec.get("company") or "").strip()
    if not v:
        return ""
    v = LEAD.sub("", v).strip(" .")
    # A legal name that merely repeats the site name is not a parent.
    if not v or v.lower() == str(rec.get("name") or "").lower():
        return ""
    # APHIS puts a certificate status in this field for some rows.
    if re.match(r"^certificate\b", v, re.I):
        return ""
    return v[:120]


def group_of(name):
    for g, rx in GROUP_RE:
        if rx.search(name or ""):
            return g
    return ""


def main():
    dry = "--dry-run" in sys.argv
    recs, missing = [], []
    for s in SOURCES:
        got = load(s)
        if got:
            recs += [dict(r, _src=s) for r in got]
        else:
            missing.append(s)
    if missing:
        print("  not harvested yet, so absent from this: %s" % ", ".join(missing))
    if not recs:
        print("No harvest files to read. Run the facility harvesters first; "
              "nothing written.", file=sys.stderr)
        return
    print("  reading %d facility records" % len(recs))

    stated = defaultdict(list)     # parent -> [child records]
    inferred = defaultdict(list)   # group  -> [child records]
    for r in recs:
        nm = str(r.get("name") or "")
        p = stated_parent(r)
        if p:
            stated[p].append(r)
            continue
        g = group_of(nm)
        if g:
            inferred[g].append(r)

    def pack(d, basis):
        out = []
        for owner, kids in sorted(d.items(), key=lambda x: -len(x[1])):
            # One site under a name is not a chain, it is a clinic. Requiring
            # two keeps the layer about ownership rather than about spelling.
            if len(kids) < 2 and basis == "inferred from the site's own name":
                continue
            countries = sorted({str(k.get("state") or "").split(",")[-1].strip()
                                for k in kids if k.get("state")})
            out.append({
                "owner": owner,
                "basis": basis,
                "sites": len(kids),
                "countries": [c for c in countries if c][:12],
                "members": [{"name": k.get("name"), "lat": k.get("lat"),
                             "lng": k.get("lng"), "where": k.get("state"),
                             "source": k.get("_src")} for k in kids],
            })
        return out

    groups = (pack(stated, "stated by the register") +
              pack(inferred, "inferred from the site's own name"))
    groups.sort(key=lambda g: -g["sites"])

    ns = sum(1 for g in groups if g["basis"].startswith("stated"))
    print("  %d owners with more than one site: %d stated by a register, "
          "%d inferred from a name" % (len(groups), ns, len(groups) - ns))
    for g in groups[:12]:
        print("     %-42s %3d sites  %-9s %s"
              % (g["owner"][:40], g["sites"],
                 "stated" if g["basis"].startswith("stated") else "inferred",
                 ", ".join(g["countries"][:3])))

    if dry:
        print("dry run \u2014 nothing written")
        return
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("Ownership as the registers state it, plus chains visible in "
                 "the names themselves. Company filings are not read here, so "
                 "this shows trading relationships rather than share "
                 "ownership."),
        "groups": groups}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d owners" % (OUT.name, len(groups)))


if __name__ == "__main__":
    main()
