#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""US fertility clinics, one point each, from CDC's ART surveillance data.

Until now the map held ONE record for the United States saying that the CDC
publishes clinic reporting. That is a fact about the register, not about the
industry, and it put a single dot on Atlanta for a sector of roughly 450 clinics
running several hundred thousand cycles a year.

The National ART Surveillance System publishes a clinic-level "Services and
Profiles" table: name, address, city, state, medical director, and which
services each clinic offers. Reporting is required of every clinic performing
ART in the United States under the Fertility Clinic Success Rate and
Certification Act, so this is close to a complete register rather than a
membership list.

The dataset id changes every year (2020 was 2577-5f9y, 2021 ui6g-vumy), so
nothing here hard-codes one. The Socrata catalogue is asked which years exist
and the newest is taken; a hard-coded id is a silent cap that goes stale
quietly, which this repository has been bitten by more than once.

    python3 harvest/cdc_art_clinics.py
    python3 harvest/cdc_art_clinics.py --dry-run
"""

import io, json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "cdc_art_clinics.json"
CACHE = HERE / "_geocache.json"

CATALOG = "https://api.us.socrata.com/api/catalog/v1"
DOMAIN = "data.cdc.gov"
WANT = "Assisted Reproductive Technology (ART) Services and Profiles"

# The Census geocoder is built for exactly this and asks nothing of us. Results
# are cached in the repository so a rerun does not re-ask for 450 addresses that
# have not moved.
CENSUS = ("https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
          "?benchmark=Public_AR_Current&format=json&address=")

# Fallback only, and it is marked as one. A state centroid is not where a clinic
# is; it is a way of not silently dropping the clinic.
STATE_CENTROID = {
    "AL": (32.81, -86.79), "AK": (61.37, -152.40), "AZ": (33.73, -111.43),
    "AR": (34.97, -92.37), "CA": (36.12, -119.68), "CO": (39.06, -105.31),
    "CT": (41.60, -72.76), "DE": (39.32, -75.51), "DC": (38.90, -77.03),
    "FL": (27.77, -81.69), "GA": (33.04, -83.64), "HI": (21.09, -157.50),
    "ID": (44.24, -114.48), "IL": (40.35, -88.99), "IN": (39.85, -86.26),
    "IA": (42.01, -93.21), "KS": (38.53, -96.73), "KY": (37.67, -84.67),
    "LA": (31.17, -91.87), "ME": (44.69, -69.38), "MD": (39.06, -76.80),
    "MA": (42.23, -71.53), "MI": (43.33, -84.54), "MN": (45.69, -93.90),
    "MS": (32.74, -89.68), "MO": (38.46, -92.29), "MT": (46.92, -110.45),
    "NE": (41.13, -98.27), "NV": (38.31, -117.06), "NH": (43.45, -71.56),
    "NJ": (40.30, -74.52), "NM": (34.84, -106.25), "NY": (42.17, -74.95),
    "NC": (35.63, -79.81), "ND": (47.53, -99.78), "OH": (40.39, -82.76),
    "OK": (35.57, -96.93), "OR": (44.57, -122.07), "PA": (40.59, -77.21),
    "PR": (18.22, -66.59), "RI": (41.68, -71.51), "SC": (33.86, -80.95),
    "SD": (44.30, -99.44), "TN": (35.75, -86.69), "TX": (31.05, -97.56),
    "UT": (40.15, -111.86), "VT": (44.05, -72.71), "VA": (37.77, -78.17),
    "WA": (47.40, -121.49), "WV": (38.49, -80.95), "WI": (44.27, -89.62),
    "WY": (42.76, -107.30),
}


def get(url, tries=3):
    for i in range(tries):
        try:
            r = Request(url, headers={"User-Agent": "GMO-map/1.0 (public research map)"})
            return urlopen(r, timeout=60).read().decode("utf-8", "replace")
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def newest_dataset():
    """Ask the catalogue which years exist and take the latest."""
    url = "%s?%s" % (CATALOG, urlencode({"domains": DOMAIN, "q": WANT, "limit": 60}))
    cat = json.loads(get(url))
    best = None
    for row in cat.get("results", []):
        res = row.get("resource") or {}
        name = res.get("name") or ""
        if "Services and Profiles" not in name:
            continue
        m = re.search(r"(19|20)\d{2}", name)
        if not m:
            continue
        year = int(m.group(0))
        if best is None or year > best[0]:
            best = (year, res.get("id"), name)
    return best


def _first(row, *names):
    """Socrata lower-cases and underscores column names, and the ART tables have
    changed their spelling between years, so several spellings are tried.

    If none of them match, the last resort is to find any column whose name
    CONTAINS the words asked for. The 2022 table used spellings none of the
    guesses covered, and the harvester dropped all 5,000 rows for want of a
    name - a silent total loss that looked like an empty register."""
    for n in names:
        for k in (n, n.lower(), n.replace(" ", "_").lower()):
            if row.get(k) not in (None, ""):
                return str(row[k]).strip()
    for n in names:
        want = [w for w in re.split(r"[^a-z]+", n.lower()) if w]
        for k, v in row.items():
            kl = str(k).lower()
            if v not in (None, "") and all(w in kl for w in want):
                return str(v).strip()
    return ""


def load_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def geocode(addr, cache):
    if addr in cache:
        return cache[addr]
    try:
        d = json.loads(get(CENSUS + quote(addr), tries=2))
        matches = (d.get("result") or {}).get("addressMatches") or []
        if matches:
            c = matches[0]["coordinates"]
            cache[addr] = [round(c["y"], 5), round(c["x"], 5)]
            return cache[addr]
    except Exception:
        pass
    cache[addr] = None
    return None


def main():
    dry = "--dry-run" in sys.argv
    found = newest_dataset()
    if not found:
        print("No ART Services and Profiles dataset found in the catalogue. The "
              "series may have been renamed; check %s and update WANT. Nothing "
              "written." % CATALOG, file=sys.stderr)
        return
    year, ds_id, name = found
    print("  newest series: %s (%s)" % (name, ds_id))

    rows = json.loads(get("https://%s/resource/%s.json?$limit=5000" % (DOMAIN, ds_id)))
    print("  %d clinic rows" % len(rows))
    if not rows:
        print("  empty response — nothing written", file=sys.stderr)
        return

    # What the table actually calls its columns, printed once. Guessing at
    # column names and dropping every row in silence is the failure this line
    # exists to prevent happening twice.
    print("  columns: %s" % ", ".join(sorted(rows[0].keys())))

    cache = load_cache()
    out, precise, approx, dropped = [], 0, 0, 0
    for r in rows:
        nm = _first(r, "clinicname", "clinic_name", "facilityname",
                    "medicalofficename", "name")
        city = _first(r, "clinicaddress2", "city", "clinic_city", "cityname")
        state = _first(r, "clinicstate", "state", "clinic_state",
                       "statename", "stateabbreviation")[:2].upper()
        street = _first(r, "clinicaddress1", "address1", "clinic_address",
                        "address", "streetaddress")
        if not nm:
            dropped += 1
            continue

        latlng, exact = None, False
        if street and city and state:
            latlng = geocode("%s, %s, %s" % (street, city, state), cache)
            exact = latlng is not None
        if latlng is None:
            latlng = STATE_CENTROID.get(state)
        if latlng is None:
            dropped += 1
            continue
        precise += 1 if exact else 0
        approx += 0 if exact else 1

        where = ", ".join([x for x in (city, state) if x])
        cycles = _first(r, "totalcycles", "total_cycles", "cycletotal")
        director = _first(r, "medicaldirector", "medical_director")
        bits = ["A fertility clinic reporting to the CDC's National ART "
                "Surveillance System."]
        if cycles:
            bits.append("It reported %s treatment cycles in %d." % (cycles, year))
        if director:
            bits.append("Medical director: %s." % director)
        bits.append("Reporting is required of every US clinic performing assisted "
                    "reproduction, under the Fertility Clinic Success Rate and "
                    "Certification Act, so this is close to a complete register "
                    "rather than a list of members. What it records is cycles "
                    "started, which is not the same as children born.")
        if not exact:
            bits.append("The address did not geocode, so this point sits at the "
                        "centre of the state rather than at the clinic.")

        out.append({
            "name": nm[:150],
            "source": "industry:repro",
            "type": "Fertility clinic",
            "lat": latlng[0], "lng": latlng[1],
            "state": where,
            "precise": bool(exact),
            # A clinic's published street address is where treatment happens -
            # unlike a university's animal-welfare registration, which is a head
            # office. Graded so the map can say which it has.
            "addr_grade": ("operational" if exact else "centroid"),
            "impact": 2,
            "company": "", "size": (("%s cycles" % cycles) if cycles else ""),
            "status": "Reporting to CDC ART surveillance",
            "phase": "post", "date": "%d-01-01" % year,
            "otype": "company",
            "tags": ["repro:clinics"], "species": ["human"],
            "url": "https://%s/resource/%s.json" % (DOMAIN, ds_id),
            "desc": " ".join(bits),
            "checked": "",
        })
        if len(out) % 50 == 0:
            time.sleep(0.5)

    print("  %d clinics: %d placed at their address, %d at a state centroid"
          % (len(out), precise, approx))
    if dropped:
        print("  %d rows had no name or no usable state and were dropped rather "
              "than placed somewhere plausible" % dropped)
    if dropped and not out:
        # Everything dropped is never a fact about the register.
        print("  EVERY row was dropped. The column names above do not match what "
              "this harvester asks for. Nothing written.", file=sys.stderr)
        return

    if dry:
        print("dry run — nothing written")
        return
    CACHE.write_text(json.dumps(cache, indent=0), encoding="utf-8")
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("Clinic-level records from CDC's ART Services and Profiles, "
                 "reporting year %d. Positions marked precise are geocoded from "
                 "the published street address; the rest sit at a state "
                 "centroid." % year),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


if __name__ == "__main__":
    main()
