#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Animal research facilities — piecing together the register that does not exist.

There is no global register. What exists is national, partial, and built on
different definitions:

  USDA APHIS  Every registered US research facility files an annual report of
              animals used by species, including how many were subjected to pain
              without relief. Published as open data. **Mice, rats and birds bred
              for research are excluded from the Animal Welfare Act's definition
              of an animal**, so the report describes a fraction of what happens.
  UK          The Home Office publishes establishment licences and annual
              procedure statistics, and separately counts animals bred and killed
              to MAINTAIN genetically altered lines - a figure nowhere else
              publishes.
  EU ALURES   27 countries, by species, purpose, severity and genetic status.

This script harvests the one of the three that is machine-readable at facility
level: the USDA annual reports. It emits one point per registered facility, with
the species counts it declared. The other two are national totals rather than
facility lists, so they stay as the hand-written entries already on the map.

Like the other discovery-based harvesters here it does not hard-code a download
URL - APHIS reorganises its data pages regularly - and it says which step failed
rather than writing a silently empty file.

    python3 harvest/animal_facilities.py --dry-run
    python3 harvest/animal_facilities.py

Writes harvest/animal_facilities.json, merged into projects.json.
"""
import io, json, re, sys, csv, pathlib
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "animal_facilities.json"

HUB = "https://www.aphis.usda.gov/pet-animal-care/annual-reports"
ALT = "https://www.aphis.usda.gov/animal-welfare/annual-reports"
UA = "GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)"

# US state centroids. Facility street addresses are published, but a laboratory's
# address is not a thing this map wants to pin precisely, and state level is what
# the release layer already uses.
ST = {
 "AL":(32.8,-86.8),"AK":(64.0,-152.0),"AZ":(34.3,-111.7),"AR":(34.9,-92.4),"CA":(37.2,-119.5),
 "CO":(39.0,-105.5),"CT":(41.6,-72.7),"DE":(39.0,-75.5),"FL":(28.6,-82.4),"GA":(32.6,-83.4),
 "HI":(20.3,-156.4),"ID":(44.4,-114.6),"IL":(40.0,-89.2),"IN":(39.9,-86.3),"IA":(42.1,-93.5),
 "KS":(38.5,-98.4),"KY":(37.5,-85.3),"LA":(31.1,-92.0),"ME":(45.4,-69.2),"MD":(39.0,-76.8),
 "MA":(42.3,-71.8),"MI":(44.3,-85.4),"MN":(46.3,-94.3),"MS":(32.7,-89.7),"MO":(38.4,-92.5),
 "MT":(47.0,-109.6),"NE":(41.5,-99.8),"NV":(39.3,-116.6),"NH":(43.7,-71.6),"NJ":(40.2,-74.7),
 "NM":(34.4,-106.1),"NY":(42.9,-75.5),"NC":(35.5,-79.4),"ND":(47.4,-100.5),"OH":(40.3,-82.8),
 "OK":(35.6,-97.5),"OR":(43.9,-120.6),"PA":(40.9,-77.8),"RI":(41.7,-71.6),"SC":(33.9,-80.9),
 "SD":(44.4,-100.2),"TN":(35.8,-86.4),"TX":(31.5,-99.3),"UT":(39.3,-111.7),"VT":(44.1,-72.7),
 "VA":(37.5,-78.9),"WA":(47.4,-120.5),"WV":(38.6,-80.6),"WI":(44.6,-89.7),"WY":(43.0,-107.6),
 "DC":(38.9,-77.0),"PR":(18.2,-66.4),
}

SPECIES = ("dogs", "cats", "primates", "guinea pigs", "hamsters", "rabbits",
           "sheep", "pigs", "other farm", "other animals")


def fetch(url, binary=False):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=120) as r:
        raw = r.read()
    return raw if binary else raw.decode("utf-8-sig", "replace")


def find_csv(page, base):
    for pat in (r'href="([^"]+\.csv)"', r'href="([^"]+annual[^"]*\.(?:csv|xlsx))"'):
        m = re.findall(pat, page, re.I)
        if m:
            u = m[0]
            return u if u.startswith("http") else (base.rsplit("/", 3)[0] + u)
    return None


def pick(row, *names):
    for n in names:
        for k, v in row.items():
            if k and n in str(k).lower() and v not in (None, ""):
                return str(v).strip()
    return ""


def to_record(row):
    state = pick(row, "state", "st").upper()[:2]
    if state not in ST:
        return None
    name = pick(row, "legal name", "customer name", "facility", "name")
    if not name:
        return None
    lat, lng = ST[state]
    counts = []
    total = 0
    for sp in SPECIES:
        v = pick(row, sp)
        try:
            n = int(float(re.sub(r"[^0-9.]", "", v) or 0))
        except Exception:
            n = 0
        if n:
            counts.append("%s %d" % (sp, n)); total += n
    pain = pick(row, "column e", "without pain relief", "pain no drugs")
    return {
        "name": (name[:120] + " \u2014 registered research facility"),
        "source": "animals:facility",
        "type": "Registered animal research facility",
        "lat": lat, "lng": lng, "state": state,
        "precise": False, "impact": 2,
        "company": "", "size": ("%d animals reported" % total) if total else "",
        "status": "Registered with USDA APHIS", "phase": "post", "date": "",
        "url": HUB,
        "desc": ("WHAT. A US research facility registered under the Animal Welfare "
                 "Act, declaring %s in its annual report%s. "
                 "WHERE IT SITS. One of roughly a thousand registered facilities, "
                 "in the only country publishing a facility-level count at all. "
                 "WHY IT MATTERS. **Mice, rats and birds bred for research are "
                 "excluded from the Act's definition of an animal.** They are the "
                 "overwhelming majority of animals used and the great majority of "
                 "genetically altered ones, so this figure describes a small "
                 "fraction of what happens here and the rest is counted nowhere."
                 % (", ".join(counts) if counts else "no covered species",
                    (", of which %s were used without pain relief" % pain) if pain else "")),
        "checked": "",
    }


def main():
    page = None
    for hub in (HUB, ALT):
        try:
            page = fetch(hub); base = hub; break
        except Exception as e:
            print("  %s unreachable (%s)" % (hub, e), file=sys.stderr)
    if page is None:
        print("could not reach either APHIS annual-report page. Nothing written.",
              file=sys.stderr); return

    url = find_csv(page, base)
    if not url:
        print("found the page but no CSV link. APHIS has reorganised; open %s and "
              "update find_csv()." % base, file=sys.stderr); return
    print("  data: %s" % url[:110])

    try:
        rows = list(csv.DictReader(io.StringIO(fetch(url))))
    except Exception as e:
        print("could not read the CSV: %s" % e, file=sys.stderr); return
    print("  %d rows" % len(rows))

    seen, out = set(), []
    for r in rows:
        rec = to_record(r)
        if not rec or rec["name"] in seen:
            continue
        seen.add(rec["name"]); out.append(rec)
    print("  facilities: %d" % len(out))

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written"); return
    OUT.write_text(json.dumps({
        "note": ("US registered animal research facilities, from APHIS annual "
                 "reports. State-level positions. Excludes mice, rats and birds "
                 "bred for research, which the Animal Welfare Act does not define "
                 "as animals - the overwhelming majority of those used."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
