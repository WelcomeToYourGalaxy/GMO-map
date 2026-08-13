#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Animal research facilities, from the national registers that name them.

Three countries publish facility-level records. Everyone else publishes a total,
a professional-society membership list, or nothing.

    United States   USDA APHIS licenses and inspects every facility using dogs,
                    cats, primates, rabbits and a few other species, and posts
                    the inspection reports and annual counts per facility by
                    name. It excludes mice, rats and birds bred for research,
                    which are the overwhelming majority of animals used - so the
                    most detailed facility register in the world omits most of
                    its subject.

    United Kingdom  The Home Office names every licensed establishment and
                    publishes annual procedure counts by species, severity and
                    purpose. This is the only place both the places and the
                    numbers are public and complete.

    European Union  ALURES collects member-state returns by species, purpose and
                    severity. It counts procedures, not places: no member state
                    is required to name its facilities.

Everywhere else, the scale of the practice is inferred from who supplies the
animals rather than reported by anyone. That is why the suppliers are on this map
as organisations and the facilities mostly are not, and it is a fact about
disclosure rather than about where the work happens.

This harvester writes the registers it can reach and names the gaps it cannot,
the same way the fertility harvester does. It does not estimate.
"""

import io, json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "animal_testing_facilities.json"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")

REGISTERS = [
    {"k": "aphis", "country": "United States", "iso": "USA", "lat": 38.90, "lng": -77.04,
     "url": "https://www.aphis.usda.gov/aphis/ourfocus/animalwelfare",
     "label": "USDA APHIS \u2014 licensed research facilities",
     "desc": ("Every registered US research facility is named, inspected, and reports "
              "annually how many dogs, cats, primates and other covered animals it used "
              "and in what pain category. The inspection reports are published per "
              "facility, specific, and almost never read. Mice, rats and birds bred for "
              "research are excluded from the governing Act, so the most detailed "
              "facility register in the world omits the overwhelming majority of the "
              "animals used in it.")},
    {"k": "homeoffice", "country": "United Kingdom", "iso": "GBR", "lat": 51.50, "lng": -0.13,
     "url": "https://www.gov.uk/government/collections/statistics-of-scientific-procedures-on-living-animals",
     "label": "Home Office \u2014 licensed establishments and annual procedures",
     "desc": ("Every UK establishment licensed to use animals in research is named in a "
              "public list, alongside annual procedure counts by species, severity and "
              "purpose. It is the only place in the world where both the places and the "
              "numbers are public and complete, and it exists because Parliament "
              "legislated for it in 1986 rather than because anyone offered it.")},
    {"k": "alures", "country": "European Union", "iso": "BEL", "lat": 50.85, "lng": 4.35,
     "url": "https://webgate.ec.europa.eu/envdataportal/web/resources/alures/submission/index",
     "label": "ALURES \u2014 EU animal use database",
     "desc": ("Member states report animal use by species, purpose and severity, and the "
              "Commission publishes the aggregate. It counts procedures rather than "
              "places: no member state is required to name its facilities, so the "
              "European picture is a set of national totals with nothing behind them.")},
    {"k": "canada", "country": "Canada", "iso": "CAN", "lat": 45.42, "lng": -75.70,
     "url": "https://ccac.ca/en/facts-and-legislation/animal-data/",
     "label": "CCAC \u2014 Canadian Council on Animal Care",
     "desc": ("Canada's system is voluntary certification by a council rather than "
              "statutory licensing. Institutions that hold federal funding must "
              "participate, aggregate numbers are published, and the certified "
              "institutions are listed \u2014 which puts Canada between the UK and the "
              "countries that publish nothing.")},
]

# Large research systems whose facilities are not publicly registered. Named,
# because an empty space on a map reads as an absence of the activity rather than
# an absence of the record.
NO_REGISTER = [
    ("China", "CHN", 35.86, 104.19,
     "A research system now comparable in scale to the American one. China publishes "
     "no national count of animals used and no facility register, so the size of the "
     "practice is inferred from the breeding suppliers rather than reported."),
    ("Japan", "JPN", 36.20, 138.25,
     "Self-regulated through institutional committees and a professional society. "
     "No national count is published, so Japanese laboratory animal use is estimated "
     "from what the suppliers sell."),
    ("India", "IND", 20.59, 78.96,
     "Experiments are overseen by a national committee that has banned animal use for "
     "cosmetics testing and some teaching, but facility-level records are not public."),
    ("South Korea", "KOR", 35.91, 127.77,
     "A large and fast-growing research sector. Aggregate figures are published "
     "annually; the institutions behind them are not named."),
    ("Brazil", "BRA", -14.24, -51.93,
     "Institutions register with a national council and aggregate figures exist, but "
     "facility-level inspection records are not published."),
    ("Russia", "RUS", 61.52, 105.31,
     "No public register of animal research facilities and no national count."),
]


def get(url, tries=2, timeout=25):
    last = None
    for i in range(tries):
        try:
            req = Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
            with urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except (URLError, HTTPError) as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise last


def main():
    out, reached = [], []
    for r in REGISTERS:
        try:
            get(r["url"], tries=1, timeout=20)
            reached.append(r["country"])
            print("  %-12s register reachable" % r["k"])
        except Exception as e:
            print("  %-12s unreachable: %s" % (r["k"], str(e)[:40]), file=sys.stderr)
        out.append({
            "name": "%s \u2014 %s" % (r["country"], r["label"]),
            "url": r["url"], "type": "Animal research facility register",
            "country": r["country"], "iso": r["iso"],
            "lat": r["lat"], "lng": r["lng"],
            "desc": r["desc"], "precise": False, "kind": "register",
        })

    for name, iso, la, ln, why in NO_REGISTER:
        out.append({
            "name": "%s \u2014 no public facility register" % name,
            "url": "", "type": "Animal research, unregistered",
            "country": name, "iso": iso, "lat": la, "lng": ln,
            "desc": why, "precise": False, "kind": "gap",
        })

    OUT.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d"),
                               "facilities": out}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print("wrote %s: %d registers, %d named gaps"
          % (OUT.name, len(REGISTERS), len(NO_REGISTER)))
    print("  reachable this run: %s" % (", ".join(reached) or "none"))
    print("  NOTE: three countries publish facility-level records. The rest publish "
          "a total or nothing, and are named as gaps rather than left blank.")


if __name__ == "__main__":
    main()
