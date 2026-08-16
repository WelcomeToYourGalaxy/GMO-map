#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""USDA APHIS animal welfare licensees and registrants, from exported CSV.

The Public Search Tool is a Salesforce app with no documented endpoint, and its
export caps at 100 rows a time. So this reads files rather than the web: drop
every CSV you export into harvest/aphis_csv/ and run this. Exporting in batches
is tedious; scraping an undocumented Aura endpoint that changes without notice
is worse, and it would break silently.

    harvest/aphis_csv/*.csv   <- any number of exports, any of the three shapes
    python3 harvest/aphis_animal_facilities.py

TWO THINGS THIS DATA IS NOT.

It is not a count of animals used. Rats, mice and birds bred for research are
excluded from the Animal Welfare Act's definition of an animal - the
overwhelming majority of animals used in research, and the great majority of the
genetically altered ones. What the Act covers is dogs, cats, primates, rabbits,
guinea pigs, hamsters and farm animals. Every record says so, because a reader
who does not know this will read the map as the whole of American animal
research when it is a fraction of it.

It is not a map of laboratories. A Class R registration is issued to a legal
entity and carries that entity's address, which for a university is the research
administration office - this export literally contains "V.P. FOR RESEARCH/1450
OLD MAIN HILL" and "Research Administration Office". The vivarium may be in
another building or another city. Class R records are therefore graded
'administrative' without exception, and dealers and breeders, whose licences
attach to premises, are graded 'operational'.
"""

import csv, json, re, sys, time, zipfile, pathlib
from urllib.request import Request, urlopen
from urllib.parse import quote
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
INDIR = HERE / "aphis_csv"
OUT = HERE / "aphis_animal_facilities.json"
CACHE = HERE / "_geocache.json"

CENSUS = ("https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
          "?benchmark=Public_AR_Current&format=json&address=")

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

# Words that mean the address on the form is a desk, not a door.
ADMIN_WORDS = re.compile(
    r"(research admin|office of|vice president|v\.?p\.?\b|p\.?o\.? box|"
    r"attn|dean|provost|chancellor|department of research|sponsored programs)", re.I)

# R is not the whole of it. Federal research facilities file under F,
# Veterans Affairs hospitals under V, and the Agricultural Research Service
# under G - 146 certificates that a filter on "Class R" misses entirely.
RESEARCH = ("R", "F", "V", "G")

CLASS_WORDS = {
    "R": "Research facility",
    "F": "Federal research facility",
    "V": "Veterans Affairs hospital",
    "G": "Agricultural Research Service facility",
    "A": "Breeder",
    "B": "Dealer",
    "C": "Exhibitor",
    "T": "Carrier",
    "H": "Intermediate handler",
}


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
        d = json.loads(get(CENSUS + quote(addr)))
        m = (d.get("result") or {}).get("addressMatches") or []
        if m:
            c = m[0]["coordinates"]
            cache[addr] = [round(c["y"], 5), round(c["x"], 5)]
            return cache[addr]
    except Exception:
        pass
    cache[addr] = None
    return None


# ---------------------------------------------------------------------------
# XLSX without a dependency.
#
# "List of active licensees and registrants" is the file that matters: 12,443
# active certificates in one download, against 100 rows a time from the search
# tool. It has no street addresses - only a mailing city and a state - so it
# gives complete coverage at low precision, and the CSV exports give high
# precision for whatever subset somebody has exported. Merging the two by
# certificate number gets both.
#
# An .xlsx is a zip of XML, so it is read here the same way the Chinese .docx
# lists are, rather than adding openpyxl to a workflow that installs nothing.
def _col(ref):
    """A1 -> 0, B1 -> 1, AA1 -> 26."""
    n = 0
    for ch in ref:
        if not ch.isalpha():
            break
        n = n * 26 + (ord(ch.upper()) - 64)
    return n - 1


def xlsx_rows(path):
    """Rows as lists, one entry per column, gaps filled.

    An empty cell is written self-closing: <c r="A12" s="7"/>. A pattern of
    <c ...>(.*?)</c> runs straight past it and swallows the NEXT cell, so every
    row came out shifted one column left with its type attribute lost - the
    licence type arrived as the raw shared-string index 15403. Self-closing
    cells are matched explicitly, and the column letter decides the position
    rather than the order cells happen to appear in.
    """
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        x = z.read("xl/sharedStrings.xml").decode("utf-8")
        for si in re.findall(r"<si>(.*?)</si>", x, re.S):
            shared.append(_unescape(re.sub(r"\s+", " ", "".join(
                re.findall(r"<t(?:\s[^>]*)?>(.*?)</t>", si, re.S))).strip()))
    sheets = sorted(n for n in z.namelist()
                    if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
    if not sheets:
        return []
    x = z.read(sheets[0]).decode("utf-8")
    out = []
    for row in re.findall(r"<row[\s>].*?</row>", x, re.S):
        cells = {}
        for attrs, body in re.findall(r"<c\b([^>]*?)(?:/>|>(.*?)</c>)", row, re.S):
            body = body or ""
            ref = re.search(r'r="([A-Z]+)', attrs)
            i = _col(ref.group(1)) if ref else len(cells)
            t = re.search(r'\bt="([^"]+)"', attrs)
            kind = t.group(1) if t else ""
            if kind == "inlineStr":
                val = _unescape("".join(
                    re.findall(r"<t(?:\s[^>]*)?>(.*?)</t>", body, re.S)))
            else:
                v = re.search(r"<v>(.*?)</v>", body, re.S)
                if not v:
                    val = ""
                elif kind == "s":
                    j = int(v.group(1))
                    val = shared[j] if 0 <= j < len(shared) else ""
                else:
                    val = _unescape(v.group(1))
            cells[i] = val.strip()
        if cells:
            width = max(cells) + 1
            out.append([cells.get(i, "") for i in range(width)])
    return out


def _unescape(s):
    return (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
             .replace("&quot;", '"').replace("&apos;", "'"))


def read_active_xlsx(path):
    """The active-list workbook. Its header is not the first row - ten lines of
    report furniture come first - so the header is found rather than assumed."""
    rows = xlsx_rows(path)
    hdr, hdr_i = None, None
    for i, r in enumerate(rows):
        if "APHIS License Number" in r:
            hdr, hdr_i = r, i
            break
    if hdr is None:
        return []
    col = {name: i for i, name in enumerate(hdr) if name}
    out = []
    for r in rows[hdr_i + 1:]:
        g = lambda name: (r[col[name]] if name in col and col[name] < len(r) else "")
        cert = g("APHIS License Number")
        if not cert:
            continue
        out.append({
            "Certificate Number": cert,
            "Registration Type": g("License Type"),
            "Account Name": g("Account Name"),
            "Site Name": g("DBA Name(s)"),
            # Mailing city, and the source says so in the column name. Never
            # promoted to an operational address.
            "City": g("Mailing City"),
            "State": g("State Abbreviation"),
            "Certificate Status": "Active",
            "Address Line 1": "", "Address Line 2": "",
            "City-State-Zip": "", "Zip": "", "County": "",
        })
    return out


def normalise(row):
    """The tool exports three different column sets. Fold them into one shape
    rather than writing three readers that drift apart."""
    g = lambda *k: next((str(row[x]).strip() for x in k
                         if row.get(x) not in (None, "")), "")
    cert = g("Certificate Number")
    kind = g("Registration Type", "License Type", "License-Registration Type")
    name = g("Account Name", "Legal Name", "Site Name")
    site = g("Site Name")
    status = g("Certificate Status")
    street = ", ".join([x for x in (g("Address Line 1"), g("Address Line 2")) if x])

    csz = g("City-State-Zip")
    city, state, zipc = g("City"), g("State"), g("Zip")
    if csz and not city:
        m = re.match(r"^(.*),\s*([A-Z]{2})\s*(\d{5})?", csz.strip())
        if m:
            city, state, zipc = m.group(1).strip(), m.group(2), (m.group(3) or "")
    if len(state) > 2:      # the inspection export writes the state in full
        state = {"alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
                 "california": "CA", "colorado": "CO", "connecticut": "CT",
                 "delaware": "DE", "florida": "FL", "georgia": "GA", "hawaii": "HI",
                 "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
                 "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME",
                 "maryland": "MD", "massachusetts": "MA", "michigan": "MI",
                 "minnesota": "MN", "mississippi": "MS", "missouri": "MO",
                 "montana": "MT", "nebraska": "NE", "nevada": "NV",
                 "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM",
                 "new york": "NY", "north carolina": "NC", "north dakota": "ND",
                 "ohio": "OH", "oklahoma": "OK", "oregon": "OR",
                 "pennsylvania": "PA", "puerto rico": "PR", "rhode island": "RI",
                 "south carolina": "SC", "south dakota": "SD", "tennessee": "TN",
                 "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA",
                 "washington": "WA", "west virginia": "WV", "wisconsin": "WI",
                 "wyoming": "WY"}.get(state.lower(), state[:2].upper())

    cls = ""
    m = re.search(r"Class\s+([A-Z])", kind)
    if m:
        cls = m.group(1)
    elif cert:
        m2 = re.match(r"\d+-([A-Z])-", cert)
        cls = m2.group(1) if m2 else ""

    return {"cert": cert, "cls": cls, "kind": kind, "name": site or name,
            "legal": name, "status": status, "street": street,
            "city": city, "state": state.upper()[:2], "zip": zipc}


def main():
    dry = "--dry-run" in sys.argv
    src = pathlib.Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else INDIR
    files = (sorted(src.glob("*.csv")) + sorted(src.glob("*.xlsx"))) if src.exists() else []
    if not files:
        print("No CSVs in %s. Export from the APHIS Public Search Tool "
              "(https://aphis.my.site.com/PublicSearchTool/s/) and put the files "
              "there. Nothing written." % src, file=sys.stderr)
        return

    # First-wins deduplication was wrong here. The tool has three export shapes
    # and only the licence and registration ones carry a street address or a
    # status; the inspection export carries neither. Keeping whichever row
    # happened to be read first threw away addresses at random. Certificates are
    # merged field by field instead, with a non-empty value beating a blank one.
    merged, order = {}, []
    for f in files:
        if f.suffix.lower() == ".xlsx":
            src_rows, n = read_active_xlsx(f), 0
            for raw in src_rows:
                r = normalise(raw)
                if not r["cert"] or not r["name"]:
                    continue
                if r["cert"] not in merged:
                    merged[r["cert"]] = r
                    order.append(r["cert"])
                    n += 1
                else:
                    have = merged[r["cert"]]
                    for k, v in r.items():
                        if v and not have.get(k):
                            have[k] = v
                    # The workbook is the authority on status: it is a list of
                    # ACTIVE certificates, so a row appearing in it outranks a
                    # stale "Cancelled" from an older export.
                    have["status"] = "Active"
            print("  %-28s %d new certificates" % (f.name[:28], n))
            continue
        with open(f, encoding="utf-8-sig", newline="") as fh:
            n = 0
            for raw in csv.DictReader(fh):
                r = normalise(raw)
                if not r["cert"] or not r["name"]:
                    continue
                if r["cert"] not in merged:
                    merged[r["cert"]] = r
                    order.append(r["cert"])
                    n += 1
                else:
                    have = merged[r["cert"]]
                    for k, v in r.items():
                        if v and not have.get(k):
                            have[k] = v
        print("  %-28s %d new certificates" % (f.name, n))
    rows = [merged[c] for c in order]

    by_cls = Counter(r["cls"] for r in rows)
    # A blank status is not an active one. The inspection export has no status
    # column at all, and treating its 97 rows as current would put dots on
    # registrations that may have lapsed years ago.
    cancelled = [r for r in rows if r["status"].lower().startswith("cancel")]
    unknown = [r for r in rows if not r["status"]]
    active = [r for r in rows if r["status"].lower().startswith("active")]
    print("  %d certificates: %s" % (len(rows), dict(by_cls)))
    print("  %d active, %d cancelled, %d with no status in any export"
          % (len(active), len(cancelled), len(unknown)))
    print("  cancelled and status-unknown are counted and not drawn. A lapsed "
          "registration is not a place doing the work today, and a certificate "
          "whose status nothing states is not evidence that it is current.")

    cache = load_cache()
    # 12,443 active certificates, one geocoder call each, is three and a half
    # hours - so the step hit its timeout and was killed before printing a
    # single line, which read in the log as "failed" with no reason given.
    #
    # Distinct cities are geocoded, not rows, and only a bounded number of new
    # ones per run. The cache is committed, so each monthly run resolves
    # another slice and the rest sit at a state centroid, marked as such. A
    # partial answer that says which part is partial beats no answer.
    # Two limits, not one. The count bounds how much work a run adds to the
    # cache; the clock bounds how long it can take. A budget alone assumes each
    # lookup costs about a second, and the moment the geocoder is slow the step
    # is killed and writes nothing - which is how this harvester failed before.
    GEOCODE_BUDGET = 900
    GEOCODE_SECONDS = 480
    started = time.time()
    todo = []
    for r in active:
        if r["street"] and r["city"] and r["state"]:
            continue
        k = "%s, %s" % (r["city"], r["state"])
        if r["city"] and r["state"] and k not in cache and k not in todo:
            todo.append(k)
    print("  %d distinct cities not yet resolved; doing up to %d this run"
          % (len(todo), GEOCODE_BUDGET))
    done = 0
    for k in todo[:GEOCODE_BUDGET]:
        if time.time() - started > GEOCODE_SECONDS:
            print("  eight minutes of lookups; stopping here and writing what "
                  "there is rather than being killed with nothing")
            break
        geocode(k, cache)
        done += 1
    if len(todo) > done:
        print("  %d cities left for the next run" % (len(todo) - done))

    out, exact_n, approx_n = [], 0, 0
    for r in active:
        latlng, exact = None, False
        if r["street"] and r["city"] and r["state"]:
            latlng = geocode("%s, %s, %s %s" % (r["street"], r["city"],
                                                r["state"], r["zip"]), cache)
            exact = latlng is not None
        if latlng is None and r["city"] and r["state"]:
            # cache only - the budget above decided what gets looked up
            latlng = cache.get("%s, %s" % (r["city"], r["state"]))
        if latlng is None:
            latlng = STATE_CENTROID.get(r["state"])
        if latlng is None:
            continue

        # A research registration is issued to an entity, not to a building.
        admin = (r["cls"] in RESEARCH) or bool(ADMIN_WORDS.search(r["street"]))
        grade = "centroid" if not exact else ("administrative" if admin else "operational")
        exact_n += 1 if grade == "operational" else 0
        approx_n += 0 if grade == "operational" else 1

        what = CLASS_WORDS.get(r["cls"], "Licensed under the Animal Welfare Act")
        bits = ["%s registered with USDA APHIS under the Animal Welfare Act, "
                "certificate %s." % (what, r["cert"])]
        if admin:
            bits.append("This is the address on the registration. A research "
                        "registration is issued to an organisation rather than to "
                        "a building, so for a university it is usually the "
                        "research administration office and the animals are "
                        "elsewhere on campus or in another city.")
        bits.append("Rats, mice and birds bred for research are excluded from the "
                    "Act's definition of an animal \u2014 the overwhelming "
                    "majority of animals used, and the great majority of the "
                    "genetically altered ones. What is covered here is dogs, cats, "
                    "primates, rabbits, guinea pigs, hamsters and farm animals. "
                    "The rest is counted nowhere.")

        out.append({
            "name": r["name"][:150],
            "source": "industry:animals",
            "type": "Animal Welfare Act " + what.lower(),
            "lat": latlng[0], "lng": latlng[1],
            "state": ", ".join([x for x in (r["city"], r["state"]) if x]),
            "precise": bool(exact and not admin),
            "addr_grade": grade,
            "impact": 3 if r["cls"] in RESEARCH else 2,
            "company": r["legal"] if r["legal"] != r["name"] else "",
            "size": "", "status": "Certificate %s" % (r["status"] or "unknown"),
            "phase": "post", "date": "",
            "otype": "institute" if r["cls"] in RESEARCH else "company",
            "tags": ["animals:services"], "species": ["lab_animals"],
            "url": "https://aphis.my.site.com/PublicSearchTool/s/",
            "desc": " ".join(bits),
            "checked": "",
        })
        if len(out) % 40 == 0:
            time.sleep(0.4)

    print("  %d drawn: %d at a street address, %d administrative or centroid"
          % (len(out), exact_n, approx_n))
    if dry:
        print("dry run \u2014 nothing written")
        return
    CACHE.write_text(json.dumps(cache, indent=0), encoding="utf-8")
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("USDA APHIS Animal Welfare Act licensees and registrants, from "
                 "exports of the Public Search Tool. Active certificates only. "
                 "Rats, mice and birds bred for research are not covered by the "
                 "Act and appear in no count anywhere."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


if __name__ == "__main__":
    main()
