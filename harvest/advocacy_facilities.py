#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Maximum-containment laboratories, and Australian animal-research facilities.

Two sources published by researchers and campaigners rather than by regulators.
That is not a lesser class of evidence and this map does not treat it as one.
Farm Transparency's list comes from freedom-of-information requests and public
licence registers - the same documents a regulator holds and does not put on a
map. Global BioLabs is a King's College London and Schar School project, peer
reviewed and cited by governments.

What DOES change is what a record should say about itself, and every record here
names where its claim comes from. That is the same treatment AAALAC gets for
being voluntary and APHIS gets for registering entities rather than buildings.
No source on this map is quoted as simply true.

WHY THESE TWO FILL REAL HOLES.

Global BioLabs maps BSL4 and BSL3+ laboratories worldwide - roughly 60 BSL4
facilities across some 27 countries, planned as well as operating. Nothing else
covers the highest-containment laboratories globally, and most of them sit in
countries whose national registers this map cannot reach at all.

Farm Transparency covers Australian animal-research facilities with addresses
and licence detail. Australia has been a blank on the animal side: CCAC covers
Canada, APHIS the United States, AAALAC the accredited minority, and nothing at
all covered Australia.

Both are file-driven, because neither publishes a stable machine endpoint:

    harvest/advocacy/*.csv          any export from either site
    python3 harvest/advocacy_facilities.py
"""

import csv, json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import quote

HERE = pathlib.Path(__file__).resolve().parent
INDIR = HERE / "advocacy"
OUT = HERE / "advocacy_facilities.json"
CACHE = HERE / "_geocache.json"

PHOTON = "https://photon.komoot.io/api/?limit=1&q="

BIOLABS = "https://www.globalbiolabs.org/map"
FARMT = "https://www.farmtransparency.org/facilities/experimentation"

AU = (-25.27, 133.78)

# Column names either export might use. Both files are hand-made rather than
# generated, so the spellings vary between downloads and guessing one is how a
# harvester silently returns nothing.
NAME = ("name", "facility", "facility name", "institution", "lab", "laboratory",
        "organisation", "organization", "site", "site name", "establishment")
CITY = ("city", "town", "locality", "suburb", "location")
COUNTRY = ("country", "nation", "state/country")
STATE = ("state", "region", "province", "territory")
ADDR = ("address", "street", "street address", "full address")
LEVEL = ("bsl", "biosafety level", "level", "containment", "bsl level")
STATUS = ("status", "operational status", "stage")


def get(url, tries=2):
    for i in range(tries):
        try:
            r = Request(url, headers={"User-Agent":
                                      "GMO-map/1.0 (public research map)"})
            return urlopen(r, timeout=60).read().decode("utf-8", "replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2)


def pick(row, names):
    low = {str(k).strip().lower(): v for k, v in row.items() if k}
    for n in names:
        if low.get(n) not in (None, ""):
            return str(low[n]).strip()
    # then any column whose name contains the word
    for n in names:
        for k, v in low.items():
            if n in k and v not in (None, ""):
                return str(v).strip()
    return ""


def load_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def geocode(q, cache):
    if q in cache:
        return cache[q]
    try:
        d = json.loads(get(PHOTON + quote(q)))
        fs = d.get("features") or []
        if fs:
            c = fs[0]["geometry"]["coordinates"]
            cache[q] = [round(c[1], 5), round(c[0], 5)]
            return cache[q]
    except Exception:
        pass
    cache[q] = None
    return None


def kind_of(row, filename):
    """Which of the two sources a row came from, decided on its content rather
    than on what somebody named the file."""
    blob = " ".join(str(v) for v in row.values()).lower() + " " + filename.lower()
    if re.search(r"\bbsl[\s\-]?[34]|biosafety level|containment", blob):
        return "biolabs"
    if re.search(r"farm ?transparency|experimentation|licen[cs]e number", blob):
        return "farmt"
    return "biolabs" if "biolab" in filename.lower() else "farmt"


def main():
    dry = "--dry-run" in sys.argv
    src = pathlib.Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else INDIR
    files = sorted(src.glob("*.csv")) if src.exists() else []
    if not files:
        print("No CSVs in %s.\n"
              "  Global BioLabs: %s (download the dataset)\n"
              "  Farm Transparency: %s (export the facility list)\n"
              "  Nothing written." % (src, BIOLABS, FARMT), file=sys.stderr)
        return

    cache = load_cache()
    out, exact_n, coarse_n, dropped = [], 0, 0, 0
    for f in files:
        rows = list(csv.DictReader(open(f, encoding="utf-8-sig", newline="")))
        if not rows:
            continue
        print("  %-30s %d rows | columns: %s"
              % (f.name[:30], len(rows), ", ".join(sorted(k for k in rows[0] if k))))
        for row in rows:
            src_kind = kind_of(row, f.name)
            nm = pick(row, NAME)
            if not nm:
                dropped += 1
                continue
            city = pick(row, CITY)
            country = pick(row, COUNTRY) or ("Australia" if src_kind == "farmt" else "")
            state = pick(row, STATE)
            street = pick(row, ADDR)

            q = ", ".join([x for x in (street, city, state, country) if x])
            latlng = geocode(q, cache) if q else None
            exact = latlng is not None and bool(street)
            if latlng is None and (city or state):
                latlng = geocode(", ".join([x for x in (city, state, country) if x]), cache)
            if latlng is None and src_kind == "farmt":
                latlng = AU
            if latlng is None:
                dropped += 1
                continue
            exact_n += 1 if exact else 0
            coarse_n += 0 if exact else 1

            if src_kind == "biolabs":
                lvl = pick(row, LEVEL)
                st = pick(row, STATUS)
                bits = ["A maximum-containment laboratory recorded by Global "
                        "BioLabs%s." % ((" at " + lvl) if lvl else "")]
                if st:
                    bits.append("Status: %s." % st)
                bits.append("Global BioLabs is a research project at King's College "
                            "London and the Schar School, not a regulator. There is "
                            "no international register of high-containment "
                            "laboratories and no obligation to declare one, so a "
                            "project like this is the only global account there is "
                            "\u2014 which also means its gaps are the gaps in what "
                            "can be found out, not in what exists.")
                rec_type = "Maximum-containment laboratory"
                tags, species, url = ["animals:services"], ["microbes"], BIOLABS
            else:
                lic = pick(row, ("licence", "license", "licence number",
                                 "license number", "permit"))
                bits = ["An animal-research facility listed by Farm Transparency "
                        "Project%s." % ((", licence " + lic) if lic else "")]
                bits.append("The list is compiled from freedom-of-information "
                            "requests and public licence registers by a campaigning "
                            "organisation. The documents behind it are the "
                            "regulator's own; what the regulator does not do is put "
                            "them on a map. Australia publishes no facility "
                            "register, so without this there is nothing.")
                rec_type = "Animal research facility"
                tags, species, url = ["animals:services"], ["lab_animals"], FARMT

            if not exact:
                bits.append("Placed at the town or region named rather than at a "
                            "street address.")

            out.append({
                "name": nm[:150],
                "source": "industry:animals",
                "type": rec_type,
                "lat": latlng[0], "lng": latlng[1],
                "state": ", ".join([x for x in (city, state, country) if x]),
                "precise": bool(exact),
                "addr_grade": "operational" if exact else "centroid",
                "impact": 3 if src_kind == "biolabs" else 2,
                "company": "", "size": "",
                "status": "Global BioLabs" if src_kind == "biolabs"
                          else "Farm Transparency Project",
                "phase": "post", "date": "", "otype": "institute",
                "tags": tags, "species": species,
                "url": url, "desc": " ".join(bits), "checked": "",
            })
            if len(out) % 40 == 0:
                time.sleep(0.6)

    print("  %d facilities: %d at an address, %d at a town or region"
          % (len(out), exact_n, coarse_n))
    if dropped:
        print("  %d rows had no name or nowhere to put them" % dropped)
    if not out:
        print("  nothing usable; the previous file is left alone", file=sys.stderr)
        return
    if dry:
        print("dry run \u2014 nothing written")
        return
    CACHE.write_text(json.dumps(cache, indent=0), encoding="utf-8")
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("Maximum-containment laboratories (Global BioLabs) and "
                 "Australian animal-research facilities (Farm Transparency "
                 "Project). Published by researchers and campaigners rather "
                 "than regulators; each record says so."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d records" % (OUT.name, len(out)))


if __name__ == "__main__":
    main()
