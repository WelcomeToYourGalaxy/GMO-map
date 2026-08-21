#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EU deliberate release notifications - the register that publishes locations.

WHY THIS ONE FIRST, of the registers still missing. The map corrected a claim
several rounds ago that Australia was the only regulator publishing field trial
sites. It is not: Directive 2001/18 requires every member state to make the
location of each release public, and several publish to the municipality or the
land parcel. Germany's Standortregister is the most precise release register in
the world.

So the map now says EU locations are published and has never fetched one. This
closes that.

WHAT IT TRIES, in order, because the Commission has moved this service twice and
a single hard-coded URL is how a harvester dies quietly:

  1. The JRC deliberate release database (GMO Register) JSON endpoint
  2. Its CSV export
  3. The notification summary listing, parsed for SNIF numbers

Each attempt is printed with what it returned. A run that finds nothing says
which of the three answered and what it held, rather than "failed" - because
"failed" is what this project's other harvesters said for weeks while returning
the wrong file.

WHAT IT DOES NOT DO. It does not invent a coordinate. A notification carries a
member state and usually a region or municipality; where the record names no
place more precise than the country, the record says so and is placed at the
country, marked coarse. Guessing a parcel from a region name would put a dot in
a field belonging to somebody who has nothing to do with it.

    python3 harvest/eu_releases.py
    python3 harvest/eu_releases.py --selftest     # no network
"""

import csv, io, json, re, sys, time, pathlib
from urllib.request import Request, urlopen

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "eu_releases.json"
UA = "GMO-map/1.0 (public research map)"

ENDPOINTS = [
    ("JRC GMO Register API",
     "https://webgate.ec.europa.eu/fip/GMO_Registers/api/notifications"),
    ("JRC GMO Register CSV",
     "https://webgate.ec.europa.eu/fip/GMO_Registers/export/notifications.csv"),
    ("Notification summary listing",
     "https://webgate.ec.europa.eu/fip/GMO_Registers/GMO_Part_B_Plants.aspx"),
]

# A SNIF number identifies one notification: B/DE/07/183, B/ES/12/34.
SNIF_RE = re.compile(r"\bB/([A-Z]{2})/(\d{2})/(\d{1,4})\b")

ISO2_NAME = {
    "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "CY": "Cyprus",
    "CZ": "Czech Republic", "DE": "Germany", "DK": "Denmark", "EE": "Estonia",
    "ES": "Spain", "FI": "Finland", "FR": "France", "GR": "Greece",
    "HR": "Croatia", "HU": "Hungary", "IE": "Ireland", "IT": "Italy",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "MT": "Malta",
    "NL": "Netherlands", "PL": "Poland", "PT": "Portugal", "RO": "Romania",
    "SE": "Sweden", "SI": "Slovenia", "SK": "Slovakia", "UK": "United Kingdom",
}


def get(url, timeout=60):
    req = Request(url, headers={"User-Agent": UA,
                                "Accept": "application/json, text/csv, text/html"})
    return urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def parse_json(body):
    try:
        d = json.loads(body)
    except Exception:
        return []
    rows = d if isinstance(d, list) else (d.get("results") or d.get("data")
                                          or d.get("notifications") or [])
    return rows if isinstance(rows, list) else []


def parse_csv(body):
    try:
        return list(csv.DictReader(io.StringIO(body)))
    except Exception:
        return []


def parse_listing(html):
    """Last resort: pull SNIF numbers and whatever sits beside them.

    Deliberately thin. A listing page gives the notification and the state and
    rarely the site, and inferring more from surrounding markup is how a
    harvester starts reporting a table cell as a location.
    """
    out, seen = [], set()
    for m in SNIF_RE.finditer(html):
        snif = m.group(0)
        if snif in seen:
            continue
        seen.add(snif)
        window = html[m.start(): m.start() + 600]
        crop = ""
        cm = re.search(r">\s*([A-Z][a-z]+ [a-z]+)\s*<", window)
        if cm:
            crop = cm.group(1)
        out.append({"snif": snif, "state": m.group(1), "crop": crop})
    return out


def field(row, *names):
    for n in names:
        for k in row:
            if str(k).strip().lower() == n.lower():
                v = row[k]
                if isinstance(v, list):
                    v = v[0] if v else ""
                if v not in (None, ""):
                    return str(v).strip()
    return ""


def normalise(rows):
    """One record per notification. No coordinate is invented."""
    out = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        snif = (field(r, "snif", "notificationNumber", "number", "reference")
                or "")
        if not snif:
            m = SNIF_RE.search(json.dumps(r, ensure_ascii=False))
            snif = m.group(0) if m else ""
        if not snif:
            continue
        m = SNIF_RE.search(snif)
        iso = (m.group(1) if m else field(r, "state", "memberState", "country"))
        country = ISO2_NAME.get(str(iso).upper(), "")
        if not country:
            continue
        place = field(r, "location", "site", "municipality", "region",
                      "commune", "nuts")
        out.append({
            "snif": snif,
            "country": country,
            "crop": field(r, "crop", "species", "organism", "plant"),
            "trait": field(r, "trait", "traits", "modification"),
            "notifier": field(r, "notifier", "applicant", "company"),
            "place": place,
            # The honest part: a record with no place named is a country-level
            # record and says so, rather than being drawn as a site.
            "precision": "site" if place else "country",
            "url": "https://webgate.ec.europa.eu/fip/GMO_Registers/",
        })
    return out


def harvest():
    rows = []
    for label, url in ENDPOINTS:
        try:
            body = get(url)
        except Exception as e:
            print("  %-30s unreachable (%s)" % (label, str(e)[:44]))
            continue
        if url.endswith(".csv"):
            got = normalise(parse_csv(body))
        elif "api" in url:
            got = normalise(parse_json(body))
        else:
            got = normalise(parse_listing(body))
        print("  %-30s answered, %d notifications" % (label, len(got)))
        if got:
            rows = got
            break

    if not rows:
        print("\nNo notifications parsed. All three routes are printed above "
              "with what each returned \u2014 an endpoint that answered and held "
              "nothing is a different problem from one that refused, and the "
              "map should not claim EU locations are harvested until one of "
              "them works.", file=sys.stderr)
        return

    sited = sum(1 for r in rows if r["precision"] == "site")
    print("\n  %d notifications across %d member states, %d with a place named"
          % (len(rows), len({r["country"] for r in rows}), sited))
    OUT.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d"),
                               "note": "Deliberate release notifications under "
                                       "Directive 2001/18. Records without a "
                                       "named place are country-level and "
                                       "marked so; no coordinate is inferred.",
                               "notifications": rows}, ensure_ascii=False,
                              indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


def selftest():
    ok = True

    def check(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %-46s %s" % (label, "pass" if good else
                              "FAIL got %r want %r" % (got, want)))

    check("SNIF parsed from a listing",
          [r["snif"] for r in parse_listing("<td>B/DE/07/183</td>")], ["B/DE/07/183"])
    check("state read off the SNIF",
          normalise([{"snif": "B/ES/12/34"}])[0]["country"], "Spain")
    check("a row with no SNIF is dropped, not guessed",
          normalise([{"crop": "maize"}]), [])
    r = normalise([{"snif": "B/DE/07/183", "municipality": "Uckermark"}])[0]
    check("a named place is site precision", r["precision"], "site")
    r2 = normalise([{"snif": "B/FR/09/2"}])[0]
    check("no place means country precision, not a guess",
          r2["precision"], "country")
    check("unknown state code dropped rather than mapped to nothing",
          normalise([{"snif": "B/ZZ/01/1"}]), [])
    print("\n%s" % ("all pass" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    harvest()
