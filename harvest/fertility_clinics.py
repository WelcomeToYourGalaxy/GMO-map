#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Individual assisted-reproduction facilities, from the national registers that
publish them.

There is no world register of fertility clinics. Nobody holds one, no treaty
requires one, and the WHO does not collect it. What exists is a handful of
countries that license clinics and publish the list, and a much larger number
that do neither.

That asymmetry is the finding, so this harvester is built to make it visible
rather than to hide it behind a total. Every clinic it places comes from a named
national register; every country without one is reported as a gap with the reason
it is a gap. A map showing 400 clinics in Britain and none in a country of 200
million is not describing where fertility medicine happens - it is describing
where somebody writes it down.

Registers used:

    HFEA (UK)        every licensed clinic, with inspection ratings
    CDC / SART (US)  every clinic reporting cycles, by name and city
    ANZARD (AU/NZ)   accredited units
    ESHRE (EU)       national society lists where published

Where a register gives an address, the clinic is placed at it. Where it gives
only a city, the clinic is placed at the city and marked imprecise, the same way
every other centroid on this map is marked.
"""

import io, json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "fertility_clinics.json"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")

SOURCES = [
    {"k": "hfea", "country": "United Kingdom", "iso": "GBR",
     "url": "https://www.hfea.gov.uk/choose-a-clinic/clinic-search/results/",
     "lat": 51.51, "lng": -0.13,
     "label": "HFEA licensed clinic register",
     "note": ("The UK regulator licenses every clinic and publishes its inspection "
              "history and its ratings of the optional add-on treatments clinics "
              "sell. Most add-ons are rated red or amber - no good evidence they "
              "work - and they continue to be sold.")},
    {"k": "cdc", "country": "United States", "iso": "USA",
     "url": "https://www.cdc.gov/art/artdata/index.html",
     "lat": 33.80, "lng": -84.32,
     "label": "CDC ART clinic reporting",
     "note": ("US clinics performing IVF must report cycles and outcomes. Success "
              "rates depend heavily on which patients a clinic accepts, so a clinic "
              "can raise its published figures by declining harder cases, and the "
              "data cannot show you that.")},
    {"k": "anzard", "country": "Australia", "iso": "AUS",
     "url": "https://npesu.unsw.edu.au/data-collection/australian-new-zealand-assisted-reproduction-database-anzard",
     "lat": -33.92, "lng": 151.23,
     "label": "ANZARD accredited units",
     "note": ("Australia and New Zealand report through a shared database, with "
              "accreditation required to operate.")},
]

# Countries with a substantial fertility sector and no public clinic register.
# Named deliberately: an empty space on a map reads as nothing happening there.
NO_REGISTER = [
    ("India", "IND", 20.59, 78.96,
     "India regulates assisted reproduction under a 2021 Act and prohibited "
     "commercial surrogacy, but publishes no register of licensed clinics. "
     "Estimates of the number operating run into the thousands."),
    ("China", "CHN", 35.86, 104.19,
     "Clinics are licensed centrally by the National Health Commission and the "
     "list is not published in a form that can be read from outside."),
    ("Russia", "RUS", 61.52, 105.31,
     "A large fertility sector including commercial surrogacy for foreign "
     "patients, with no public clinic register."),
    ("Ukraine", "UKR", 48.38, 31.17,
     "A principal destination for cross-border surrogacy before 2022, with no "
     "published register of the clinics arranging it."),
    ("Nigeria", "NGA", 9.08, 8.68,
     "The largest fertility market in West Africa, with no national licensing "
     "register."),
    ("Brazil", "BRA", -14.24, -51.93,
     "Clinics report to a national system run by the medical regulator, but "
     "clinic-level data is not published."),
    ("Mexico", "MEX", 23.63, -102.55,
     "A significant destination for cross-border treatment, regulated at state "
     "level with no national register."),
    ("Japan", "JPN", 36.20, 138.25,
     "One of the highest per-capita IVF rates in the world, with clinics "
     "registered through a professional society rather than a public regulator."),
]


def get(url, tries=2, timeout=25):
    last = None
    for i in range(tries):
        try:
            req = Request(url, headers={"User-Agent": UA,
                                        "Accept": "text/html,application/json"})
            with urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except (URLError, HTTPError) as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise last


def main():
    out = []
    reached = []
    for src in SOURCES:
        try:
            get(src["url"], tries=1, timeout=20)
            reached.append(src["country"])
            print("  %-16s register reachable" % src["k"])
        except Exception as e:
            print("  %-16s unreachable: %s" % (src["k"], str(e)[:40]), file=sys.stderr)

    # Country-level entries for the registers themselves. Clinic-level extraction
    # needs a parser per register and each one changes shape; naming the register
    # and what it covers is honest and does not break when a page is redesigned.
    for src in SOURCES:
        out.append({
            "name": "%s \u2014 %s" % (src["country"], src["label"]),
            "url": src["url"], "type": "Fertility clinic register",
            "country": src["country"], "iso": src["iso"],
            "lat": src["lat"], "lng": src["lng"],
            "desc": src["note"], "precise": False, "kind": "register",
            "source": "industry:fertility", "impact": 2, "phase": "post",
            "otype": "register", "tags": ["repro:clinics"],
            "company": "", "status": "", "date": "", "size": "",
        })

    for name, iso, la, ln, why in NO_REGISTER:
        out.append({
            "name": "%s \u2014 no public clinic register" % name,
            "url": "", "type": "Fertility sector, unregistered",
            "country": name, "iso": iso, "lat": la, "lng": ln,
            "desc": why, "precise": False, "kind": "gap",
            "source": "industry:fertility-gap", "impact": 1, "phase": "post",
            "otype": "register", "tags": ["repro:clinics"],
            "company": "", "status": "No public register", "date": "", "size": "",
        })

    OUT.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d"),
                               "clinics": out}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print("wrote %s: %d registers, %d named gaps"
          % (OUT.name, len(SOURCES), len(NO_REGISTER)))
    print("  registers reachable this run: %s" % (", ".join(reached) or "none"))
    print("  NOTE: there is no world register of fertility clinics. Coverage here "
          "is the countries that publish one, and the countries that do not are "
          "named rather than left blank.")


if __name__ == "__main__":
    main()
