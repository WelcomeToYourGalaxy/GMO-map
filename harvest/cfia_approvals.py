#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harvest Canadian unconfined-release approvals into the release layer.

Source: the CFIA's "Plants with Novel Traits (PNT) and Novel Feeds from Plant
Sources Approved in Canada" dataset, published on open.canada.ca under the Open
Government Licence with a direct CSV endpoint:

  https://active.inspection.gc.ca/netapp/plantnoveltraitpnt-vegecarnouvcn/pntvcne.aspx?download=csv

Verified header (note the typo "TME" is in the source, not here):
  PLANT, PRODUCT, OECD, LMO, APPLICANT AT TME OF APPLICATION, NOVEL TRAITS,
  CFIA APPROVAL FOR UNCONFINED RELEASE, APPROVAL FOR LIVESTOCK FEED,
  HEALTH CANADA FOOD SAFETY APPROVAL

Two things make this register worth having beyond one more country:

1. It carries the **OECD unique identifier** for most events. That is the string
   the map keeps telling people to write down, because it is what links one
   engineered event across every country that has ruled on it. No other feed
   here supplies it.

2. Canada regulates by **novelty of trait, not by technique**, so the same
   register lists transgenic events (LMO) and products of mutagenesis and gene
   editing (Non-LMO) side by side. Everywhere else the second group is
   increasingly written out of registration entirely. This is the one register
   that shows both, and the LMO column says which is which.

Only rows approved for unconfined release in Canada are kept. "Not grown in
Canada" means the event was cleared for feed or food import and never for
planting - the same import-versus-release distinction the APHIS harvester makes.

    python3 harvest/cfia_approvals.py --dry-run
    python3 harvest/cfia_approvals.py            # writes harvest/cfia_records.json

Output is merged into projects.json by aphis_releases.py. Standard library only.
"""
import csv, io, json, re, sys, pathlib
from datetime import date, datetime
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "cfia_records.json"
URL = ("https://active.inspection.gc.ca/netapp/plantnoveltraitpnt-vegecarnouvcn/"
       "pntvcne.aspx?download=csv&product=&applicant=&trait=&designation=")
UA = "Mozilla/5.0 (compatible; GMO-map CFIA harvester; +https://github.com/WelcomeToYourGalaxy/GMO-map)"

# Canada has no province in this dataset, so every record sits at the national
# centroid and is marked imprecise. Same rule as APHIS: never imply a site.
CA_LAT, CA_LNG = 56.13, -106.35

# Values in the approval column that are NOT an approval to plant in Canada.
NOT_APPROVED = ("not grown in canada", "no application received",
                "application withdrawn", "not considered novel",
                "not assessed", "under review", "withdrawn")

DATE_RX = re.compile(r"([A-Z][a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})")
# An OECD unique identifier is applicant code - event code - check digit, e.g.
# MON-00179-5 or BCS-GH\u00d8\u00d824-7 (the register uses \u00d8 for zero, as the
# standard does). Free text and repeated product names also appear in that
# column, so match the shape instead of testing for non-empty.
OECD_RX = re.compile(r"\b[A-Z][A-Z0-9]{1,3}-[A-Z0-9\u00d8]{4,7}-\d\b")
DD_RX = re.compile(r"(DD\d{2,4}-\d+)")


def fetch():
    req = Request(URL, headers={"User-Agent": UA})
    with urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8-sig", "replace")


def col(row, *names):
    """The source header has a typo ("TME" for "TIME") and inconsistent spacing.
    Match on a normalised key rather than an exact string."""
    norm = {re.sub(r"[^a-z]", "", (k or "").lower()): v for k, v in row.items()}
    for n in names:
        v = norm.get(re.sub(r"[^a-z]", "", n.lower()))
        if v:
            return v.strip()
    return ""


def approval_date(text):
    m = DATE_RX.search(text or "")
    if not m:
        return ""
    try:
        return datetime.strptime("%s %s %s" % m.groups(), "%B %d %Y").date().isoformat()
    except ValueError:
        return ""


def is_approved(text):
    t = (text or "").strip().lower()
    if not t:
        return False
    if any(bad in t for bad in NOT_APPROVED):
        return False
    # "Yes (July 28, 2005) DD2005-53" or a bare date, as some rows carry
    return t.startswith("yes") or bool(DATE_RX.search(text))


def build(rows):
    out = []
    for r in rows:
        plant = col(r, "PLANT")
        approval = col(r, "CFIA APPROVAL FOR UNCONFINED RELEASE")
        if not plant or not is_approved(approval):
            continue
        product = col(r, "PRODUCT")
        oecd = col(r, "OECD")
        lmo = col(r, "LMO")
        applicant = col(r, "APPLICANT AT TME OF APPLICATION", "APPLICANT") or "Not stated"
        traits = col(r, "NOVEL TRAITS")
        feed = col(r, "APPROVAL FOR LIVESTOCK FEED")
        food = col(r, "HEALTH CANADA FOOD SAFETY APPROVAL")

        when = approval_date(approval)
        dd = DD_RX.search(approval)
        transgenic = lmo.strip().lower() == "lmo"

        ids = OECD_RX.findall(oecd or "")
        ident = ((" OECD unique identifier%s %s \u2014 the string that links this same event "
                  "to every other country that has ruled on it."
                  % ("s" if len(ids) > 1 else "", ", ".join(ids))) if ids else
                 (" No OECD unique identifier. Those are assigned to transgenic events; "
                  "an organism made by mutagenesis or gene editing has no transgene to "
                  "identify, so it cannot be tracked across borders by that route at all."))

        technique = ("Transgenic (recorded as an LMO)." if transgenic else
                     "Recorded as Non-LMO \u2014 a product of mutagenesis or gene editing. "
                     "Canada regulates by novelty of trait rather than by technique, so it "
                     "appears in the same register as transgenic events. In most other "
                     "jurisdictions this class is increasingly outside registration entirely.")

        desc = ("Approved for unconfined environmental release in Canada%s. Applicant at "
                "the time of application: %s.%s %s%s%s Position is the national centroid \u2014 "
                "this register records a national approval, not a planting location."
                % ((" on " + when) if when else "", applicant,
                   (" Traits: " + traits + ".") if traits else "",
                   technique, ident,
                   (" Livestock feed: %s. Food: %s." % (feed, food)) if (feed or food) else ""))

        out.append({
            "name": "%s \u2014 %s (%s)" % (plant, product or "event not named", applicant),
            "source": "cfia:pnt",
            "type": "%s, unconfined release approval" % plant,
            "lat": CA_LAT, "lng": CA_LNG,
            "state": "Canada (national approval)",
            "precise": False,
            "impact": 5,          # an unconfined release approval is national and open-ended
            "company": applicant,
            "size": "National approval for unconfined release, no area limit",
            "status": "Approved for unconfined release" + ((" " + dd.group(1)) if dd else ""),
            "phase": "post",
            "date": when,
            "oecd": ids,              # list, possibly empty - never inferred from prose
            "oecd_raw": oecd,         # the cell as published, for auditing misses
            "transgenic": transgenic,
            "url": "https://inspection.canada.ca/en/plant-varieties/plants-novel-traits/approved-under-review",
            "desc": desc,
        })
    return out


def main():
    try:
        text = fetch()
    except Exception as e:
        print("could not fetch CFIA dataset: %s" % e, file=sys.stderr)
        sys.exit(1)
    rows = list(csv.DictReader(io.StringIO(text)))
    recs = build(rows)
    print("  cfia      %6d rows \u2192 %5d approved for unconfined release" % (len(rows), len(recs)))

    # Cross-tab rather than two separate counts, because the interesting question
    # is whether the identifier tracks the technique - and if it does, the class
    # being deregulated worldwide is also the class that cannot be followed
    # across borders. Measured, not assumed.
    # Cross-tab on the record's own fields. An earlier version tested for the
    # phrase "OECD unique identifier" inside the description - which also appears
    # in the sentence "No OECD unique identifier", so every record counted as
    # having one and the table was meaningless. Never measure prose.
    tab = {(True, True): 0, (True, False): 0, (False, True): 0, (False, False): 0}
    for r in recs:
        tab[(bool(r["transgenic"]), bool(r["oecd"]))] += 1
    lmo = tab[(True, True)] + tab[(True, False)]
    print("    %d transgenic, %d products of mutagenesis or gene editing" % (lmo, len(recs) - lmo))
    print("    identifier by technique:")
    print("      transgenic  with id %3d   without %3d" % (tab[(True, True)], tab[(True, False)]))
    print("      non-LMO     with id %3d   without %3d" % (tab[(False, True)], tab[(False, False)]))
    if tab[(False, True)] == 0 and tab[(True, False)] == 0:
        print("      \u2192 the identifier tracks the technique exactly in this register:")
        print("        every transgenic event has one, no gene-edited or mutagenesis")
        print("        product does.")
    else:
        print("      \u2192 the identifier does NOT track the technique cleanly here.")
        if tab[(False, True)]:
            print("        %d non-LMO products carry one." % tab[(False, True)])
        if tab[(True, False)]:
            print("        %d transgenic events lack one:" % tab[(True, False)])
            # Print them. A transgenic event with no identifier is either genuinely
            # unassigned or a formatting quirk in the source cell, and those mean
            # different things - so show the cell rather than characterising it.
            for r in recs:
                if r["transgenic"] and not r["oecd"]:
                    print("          %-42s OECD cell: %s"
                          % (r["name"][:42], repr(r["oecd_raw"]) if r["oecd_raw"] else "(empty)"))
    crops = {}
    for r in recs:
        crops[r["type"].split(",")[0]] = crops.get(r["type"].split(",")[0], 0) + 1
    print("    crops: " + ", ".join("%s %d" % (k, v)
          for k, v in sorted(crops.items(), key=lambda x: -x[1])[:8]))

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written")
        for r in recs[:3]:
            print("\n  " + r["name"][:72])
            print("  " + r["desc"][:200])
        return
    OUT.write_text(json.dumps({
        "note": ("Canadian unconfined-release approvals from the CFIA PNT dataset "
                 "(open.canada.ca, Open Government Licence). Merged into projects.json "
                 "by aphis_releases.py. National approvals, so every record is at the "
                 "country centroid and marked imprecise."),
        "generated": date.today().isoformat(),
        "projects": recs,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s: %d records" % (OUT.name, len(recs)))


if __name__ == "__main__":
    main()
