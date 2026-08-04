#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Human clinical — harvested rather than hand-written.

The clinical facet had the worst coverage ratio on the map: ~31 hand-written
entries against thousands of organisations running gene and cell therapy trials.
Hand-entry was never going to close that, and it did not need to, because
**this is the one facet with a complete public register.**

ClinicalTrials.gov requires registration of essentially every interventional
trial run in or submitted to the US, and carries non-US trials besides. Its v2
API is open, needs no key, and returns sponsor, phase, status, condition and
every recruiting location. This script aggregates it BY SPONSOR: one point per
organisation, carrying how many gene or cell therapy trials it runs and what
stage they have reached.

That turns a facet the map sampled into one it covers.

What it does not do: claim to be the world. Trials run entirely outside the US
regulatory orbit may never appear here, and China in particular is
under-represented relative to its actual programme. The note in the output says
so, and the map should not imply otherwise.

    python3 harvest/clinical_sponsors.py --dry-run
    python3 harvest/clinical_sponsors.py --min-trials 3

Writes harvest/clinical_sponsors.json.
"""
import io, json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlencode

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "clinical_sponsors.json"

API = "https://clinicaltrials.gov/api/v2/studies"
UA = "GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)"

# The searches that define this facet. Kept explicit rather than one broad query,
# because "gene therapy" alone misses cell therapy and editing trials that never
# use the phrase.
QUERIES = (
    "gene therapy", "gene editing", "CRISPR", "CAR-T", "cell therapy",
    "lentiviral vector", "adeno-associated virus vector", "base editing",
    "gene transfer", "genetically modified cells",
)

# Sponsor country is not a field, so it is read from the first location. These
# are the country names ClinicalTrials.gov actually writes.
CENTROID = {
 "United States": (39.8, -98.6), "China": (35.9, 104.2), "Japan": (36.2, 138.3),
 "United Kingdom": (55.4, -3.4), "Germany": (51.2, 10.5), "France": (46.2, 2.2),
 "Canada": (56.1, -106.3), "Australia": (-25.3, 133.8), "Spain": (40.5, -3.7),
 "Italy": (41.9, 12.6), "Netherlands": (52.1, 5.3), "Belgium": (50.5, 4.5),
 "Switzerland": (46.8, 8.2), "Sweden": (60.1, 18.6), "Denmark": (56.3, 9.5),
 "Norway": (60.5, 8.5), "Israel": (31.0, 34.9), "Korea, Republic of": (35.9, 127.8),
 "Taiwan": (23.7, 121.0), "India": (20.6, 79.0), "Brazil": (-14.2, -51.9),
 "Singapore": (1.35, 103.8), "Poland": (51.9, 19.1), "Austria": (47.5, 14.6),
 "Ireland": (53.4, -8.2), "Turkey": (39.0, 35.2), "Russia": (61.5, 105.3),
 "Egypt": (26.8, 30.8), "Mexico": (23.6, -102.6), "Argentina": (-34.6, -58.4),
 "New Zealand": (-40.9, 174.9), "Finland": (61.9, 25.7), "Czechia": (49.8, 15.5),
 "Portugal": (39.4, -8.2), "Greece": (39.1, 21.8), "Hungary": (47.2, 19.5),
 "Thailand": (15.9, 101.0), "Malaysia": (4.2, 101.98), "Iran": (32.4, 53.7),
 "Saudi Arabia": (23.9, 45.1), "South Africa": (-30.6, 22.9), "Chile": (-35.7, -71.5),
}


def get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            last = e; time.sleep(3 * (i + 1))
    raise last


def studies_for(term, page_size=1000, max_pages=12):
    """Paginate one query. The API returns a nextPageToken; follow it."""
    token, out, pages = None, [], 0
    while pages < max_pages:
        q = {"query.term": term, "pageSize": page_size,
             "fields": ("protocolSection.identificationModule.nctId,"
                        "protocolSection.sponsorCollaboratorsModule.leadSponsor.name,"
                        "protocolSection.sponsorCollaboratorsModule.leadSponsor.class,"
                        "protocolSection.designModule.phases,"
                        "protocolSection.statusModule.overallStatus,"
                        "protocolSection.contactsLocationsModule.locations")}
        if token:
            q["pageToken"] = token
        data = get(API + "?" + urlencode(q))
        got = data.get("studies") or []
        out.extend(got)
        token = data.get("nextPageToken")
        pages += 1
        if not token or not got:
            break
        time.sleep(0.5)
    return out


def dig(d, *path):
    for p in path:
        if not isinstance(d, dict):
            return None
        d = d.get(p)
    return d


def main():
    min_trials = 2
    if "--min-trials" in sys.argv:
        min_trials = int(sys.argv[sys.argv.index("--min-trials") + 1])

    seen_nct, spon = set(), {}
    for term in QUERIES:
        try:
            studies = studies_for(term)
        except Exception as e:
            print("  query %-28s failed: %s" % (term, str(e)[:50]), file=sys.stderr)
            continue
        new = 0
        for st in studies:
            ps = st.get("protocolSection") or {}
            nct = dig(ps, "identificationModule", "nctId")
            if not nct or nct in seen_nct:
                continue
            seen_nct.add(nct); new += 1
            name = dig(ps, "sponsorCollaboratorsModule", "leadSponsor", "name")
            if not name:
                continue
            rec = spon.setdefault(name.strip(), {
                "name": name.strip(),
                "sclass": dig(ps, "sponsorCollaboratorsModule", "leadSponsor", "class") or "",
                "trials": 0, "phases": {}, "status": {}, "countries": {}})
            rec["trials"] += 1
            for ph in (dig(ps, "designModule", "phases") or ["NA"]):
                rec["phases"][ph] = rec["phases"].get(ph, 0) + 1
            stt = dig(ps, "statusModule", "overallStatus") or ""
            if stt:
                rec["status"][stt] = rec["status"].get(stt, 0) + 1
            for loc in (dig(ps, "contactsLocationsModule", "locations") or [])[:6]:
                c = (loc or {}).get("country")
                if c:
                    rec["countries"][c] = rec["countries"].get(c, 0) + 1
        print("  %-28s %5d studies (%d new) \u2192 %d sponsors so far"
              % (term, len(studies), new, len(spon)))

    print("\n  %d trials, %d distinct lead sponsors" % (len(seen_nct), len(spon)))

    out, noplace = [], 0
    for rec in spon.values():
        if rec["trials"] < min_trials:
            continue
        country = max(rec["countries"], key=rec["countries"].get) if rec["countries"] else ""
        pos = CENTROID.get(country)
        if not pos:
            noplace += 1; continue
        ph = ", ".join("%s\u00d7%d" % (k.replace("PHASE", "Phase "), v)
                       for k, v in sorted(rec["phases"].items(), key=lambda x: -x[1])[:4])
        recruiting = rec["status"].get("RECRUITING", 0)
        kind = {"INDUSTRY": "company", "NIH": "ministry", "FED": "ministry",
                "OTHER_GOV": "ministry", "NETWORK": "association",
                "INDIV": "institute", "OTHER": "institute"}.get(rec["sclass"], "institute")
        out.append({
            "name": rec["name"][:150],
            "source": "clinical:sponsor",
            "type": "Gene or cell therapy trial sponsor",
            "lat": pos[0], "lng": pos[1], "state": country,
            "precise": False, "impact": 2 if rec["trials"] < 10 else 3,
            "company": "", "size": "%d trials" % rec["trials"],
            "status": "%d recruiting" % recruiting if recruiting else "No trial recruiting",
            "phase": "post", "date": "", "otype": kind,
            "url": "https://clinicaltrials.gov/search?term=" +
                   rec["name"].replace(" ", "+")[:80],
            "desc": ("WHAT. Lead sponsor of %d registered gene or cell therapy trials (%s). "
                     "WHERE IT SITS. One organisation inside the only facet on this map with "
                     "a complete public register \u2014 registration is required for essentially "
                     "every interventional trial run in or submitted to the United States. "
                     "WHY IT MATTERS. The register exists because a law requires it, after "
                     "sponsors were found abandoning trials with unfavourable results "
                     "unpublished. Every other facet here is argued about with figures the "
                     "industry chose to release; this one is not."
                     % (rec["trials"], ph or "phase not stated")),
            "checked": "",
        })

    print("  sponsors with %d+ trials and a placeable country: %d" % (min_trials, len(out)))
    if noplace:
        print("  dropped for no locatable country: %d" % noplace)

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written"); return
    OUT.write_text(json.dumps({
        "note": ("Gene and cell therapy trial sponsors from ClinicalTrials.gov v2 API, "
                 "aggregated one point per lead sponsor at the country of its most "
                 "frequent trial location. NOT a world census: trials run entirely "
                 "outside the US regulatory orbit may never register here, and China "
                 "is under-represented relative to its actual programme."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
