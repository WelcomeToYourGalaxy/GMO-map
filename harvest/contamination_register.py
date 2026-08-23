#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recover the GM Contamination Register, 1997-2013.

The Register itself stopped being updated in 2013 and its site has been
unreliable since, which is why the escape layer on this map was hand-compiled.
But the whole dataset survives in the open literature:

    Price B & Cotter J (2014). "The GM Contamination Register: a review of
    recorded contamination incidents associated with genetically modified
    organisms (GMOs), 1997-2013." International Journal of Food Contamination
    1:5. doi:10.1186/s40550-014-0005-8

It is open access under CC BY, and **Additional file 1 is the incident table** -
all 396 incidents across 63 countries. That is the source this script pulls.

It does NOT hard-code a download URL. Supplementary-file URLs move; the article
DOI does not. So it fetches the article page, finds the supplementary link, and
follows it. If the layout changes the script says exactly which step failed
rather than writing a silently empty file.

    python3 harvest/contamination_register.py --dry-run
    python3 harvest/contamination_register.py

Writes harvest/register_records.json in the same shape as escape_records.json,
which the map merges alongside the hand-compiled incidents. Records already in
escape_records.json are skipped by name so the detailed hand-written entries win
over the register's one-line summaries.

Licence note: CC BY requires attribution, which every emitted record carries in
its `desc` and `url`.
"""
import io, json, re, sys, pathlib
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "register_records.json"
HAND = ROOT / "harvest" / "escape_records.json"

DOI = "10.1186/s40550-014-0005-8"

# The Register stopped in 2013. Nothing replaced it, so the honest incident
# picture is several partial sources stacked, each stating its own scope:
#
#   GM Contamination Register  1997-2013, 396 incidents, 63 countries. Compiled
#                              by GeneWatch UK and Greenpeace. The only global
#                              compilation that has ever existed.
#   RASFF                      EU border rejections of unauthorised GM material.
#                              Current and official, but EU imports only.
#   Testbiotech / GMWatch      Case write-ups rather than a dataset - useful for
#                              detail on a specific incident, not for coverage.
#
# All of them together are still not a world picture, and every record says so.
EXTRA_SOURCES = [
    ("RASFF", "https://webgate.ec.europa.eu/rasff-window/screen/search",
     "EU border rejections of unauthorised GM material. Official and current, "
     "but it records what was stopped entering the European Union - not what "
     "happened elsewhere, and not what was never caught."),
    ("Testbiotech", "https://www.testbiotech.org/en/", None),
    ("GMWatch", "https://gmwatch.org/en/gm-contamination-register", None),
]
# The journal moved. It published as International Journal of Food Contamination
# and is now Food Safety and Risk on BioMed Central, so the Springer path no
# longer resolves and the supplementary link went with it. The data is
# "Additional file 1" on the article page. Candidates tried in order.
# Springer Nature Link FIRST: the journal migrated there and the BioMed Central
# address, while still answering, serves a page with no supplement link on it.
ARTICLE = "https://link.springer.com/article/" + DOI
ARTICLE_ALTS = [
    "https://foodsafetyandrisk.biomedcentral.com/articles/" + DOI,
    "https://doi.org/" + DOI,
    "https://foodsafetyandrisk.biomedcentral.com/counter/pdf/" + DOI + ".pdf",
]
UA = ("GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map) "
      "recovering an open-access supplementary dataset")

CITE = ("Recorded in the GM Contamination Register (GeneWatch UK / Greenpeace "
        "International), as published in Price & Cotter 2014, Int. J. Food "
        "Contamination 1:5, CC BY.")

# Country centroids for the countries the Register covers. Region-level only:
# the Register records the country an incident was found in, not a site.
CENTROID = {
 "argentina": (-34.6, -58.4), "australia": (-25.3, 133.8), "austria": (47.5, 14.6),
 "bangladesh": (23.7, 90.4), "belgium": (50.5, 4.5), "bolivia": (-16.3, -63.6),
 "brazil": (-14.2, -51.9), "bulgaria": (42.7, 25.5), "canada": (56.1, -106.3),
 "chile": (-35.7, -71.5), "china": (35.9, 104.2), "colombia": (4.6, -74.3),
 "costa rica": (9.7, -83.8), "croatia": (45.1, 15.2), "cyprus": (35.1, 33.4),
 "czech republic": (49.8, 15.5), "denmark": (56.3, 9.5), "ecuador": (-1.8, -78.2),
 "egypt": (26.8, 30.8), "finland": (61.9, 25.7), "france": (46.2, 2.2),
 "germany": (51.2, 10.5), "greece": (39.1, 21.8), "hungary": (47.2, 19.5),
 "india": (20.6, 79.0), "indonesia": (-0.8, 113.9), "ireland": (53.4, -8.2),
 "italy": (41.9, 12.6), "japan": (36.2, 138.3), "kenya": (-0.02, 37.9),
 "latvia": (56.9, 24.6), "lithuania": (55.2, 23.9), "luxembourg": (49.8, 6.1),
 "mexico": (23.6, -102.6), "netherlands": (52.1, 5.3), "new zealand": (-40.9, 174.9),
 "nigeria": (9.1, 8.7), "norway": (60.5, 8.5), "pakistan": (30.4, 69.3),
 "paraguay": (-23.4, -58.4), "peru": (-9.2, -75.0), "philippines": (12.9, 121.8),
 "poland": (51.9, 19.1), "portugal": (39.4, -8.2), "romania": (45.9, 25.0),
 "russia": (61.5, 105.3), "saudi arabia": (23.9, 45.1), "serbia": (44.0, 21.0),
 "singapore": (1.35, 103.8), "slovakia": (48.7, 19.7), "slovenia": (46.2, 15.0),
 "south africa": (-30.6, 22.9), "south korea": (35.9, 127.8), "spain": (40.5, -3.7),
 "sweden": (60.1, 18.6), "switzerland": (46.8, 8.2), "taiwan": (23.7, 121.0),
 "thailand": (15.9, 101.0), "turkey": (39.0, 35.2), "ukraine": (48.4, 31.2),
 "united kingdom": (55.4, -3.4), "uk": (55.4, -3.4), "united states": (39.8, -98.6),
 "usa": (39.8, -98.6), "vietnam": (14.1, 108.3), "zambia": (-13.1, 27.8),
}


def fetch(url, binary=False):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=120) as r:
        raw = r.read()
    return raw if binary else raw.decode("utf-8", "replace")


def find_supplement(page):
    """The link to Additional file 1, wherever the layout has put it."""
    pats = [r'href="(https://static-content\.springer\.com/esm/[^"]+)"',
            r'href="(/articles/[^"]*?/MediaObjects/[^"]+)"',
            r'href="([^"]*MediaObjects[^"]+\.(?:xlsx|xls|csv|pdf|docx))"']
    for p in pats:
        m = re.findall(p, page, re.I)
        if m:
            u = m[0]
            return u if u.startswith("http") else ("https://link.springer.com" + u)
    return None


def rows_from_csv(text):
    import csv
    return list(csv.DictReader(io.StringIO(text)))


def rows_from_xlsx(data):
    try:
        import openpyxl
    except ImportError:
        print("  ! openpyxl not installed - `pip install openpyxl` to read the "
              "spreadsheet supplement", file=sys.stderr)
        return []
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        f.write(data); path = f.name
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    head = [str(h or "").strip().lower() for h in rows[0]]
    return [dict(zip(head, r)) for r in rows[1:] if any(r)]


def pick(row, *names):
    for n in names:
        for k, v in row.items():
            if k and n in str(k).lower() and v:
                return str(v).strip()
    return ""


def to_record(row, seq):
    country = pick(row, "country", "location", "region")
    year = pick(row, "year", "date")
    crop = pick(row, "crop", "species", "organism")
    what = pick(row, "description", "incident", "detail", "summary", "type")
    if not (country or crop):
        return None
    key = re.sub(r"[^a-z ]", "", country.lower()).strip()
    lat, lng = CENTROID.get(key, (None, None))
    if lat is None:
        return None
    y = re.search(r"(19|20)\d{2}", str(year) or "")
    name = "%s \u2014 %s contamination incident%s" % (
        country, crop or "GM", (" (%s)" % y.group(0)) if y else "")
    return {
        "name": name[:180],
        "source": "escape:register",
        "type": (crop or "Unspecified") + ", recorded contamination incident",
        "lat": lat, "lng": lng, "state": country, "precise": False,
        "impact": 2, "company": "", "size": "",
        "status": "Recorded 1997\u20132013", "phase": "post",
        "date": ("%s-01-01" % y.group(0)) if y else "",
        "url": "https://doi.org/" + DOI,
        "desc": ("WHAT. %s WHERE IT SITS. One of 396 incidents across 63 countries "
                 "recorded between 1997 and 2013. WHY IT MATTERS. The Register "
                 "stopped in 2013 and nothing replaced it, so this is the whole "
                 "systematic record that exists \u2014 and it was compiled by two "
                 "campaigning organisations rather than by any regulator. %s"
                 % ((what or ("Recorded contamination involving %s in %s."
                              % (crop or "GM material", country)))[:400], CITE)),
        "checked": "",
    }


def main():
    # THIS LOOP USED TO BREAK ON THE FIRST PAGE THAT FETCHED, not on the first
    # page that carried what it came for. The journal moved to Springer Nature
    # Link, and the old BioMed Central address still answers - with a page that
    # has no supplementary-file link on it. So the run "reached" the article,
    # found no supplement, and exited telling us the layout had changed, three
    # weeks running, while the alternate that would have worked sat untried in
    # the list below it. Reaching a page is not the same as getting the thing.
    print("fetching the article page")
    page, link, reached = None, None, []
    for _cand in ([ARTICLE] + ARTICLE_ALTS):
        try:
            page = fetch(_cand)
        except Exception as e:
            print("  %-66s %s" % (_cand[:66], str(e)[:32]), file=sys.stderr)
            continue
        link = find_supplement(page)
        reached.append((_cand, bool(link)))
        print("  reached %-58s supplement link: %s"
              % (_cand[:58], "yes" if link else "no"))
        if link:
            break
    if not reached:
        sys.exit("every article route refused. Nothing written: an empty file would "
                 "reach the map as no recorded incidents, which is the opposite of "
                 "true. A 403 everywhere usually means the request was blocked; a "
                 "404 would mean the article moved again.")
    if not link:
        sys.exit("reached %d of the article's addresses and none carried a "
                 "supplementary-file link: %s. The DOI is stable, so the article has "
                 "not gone - the layout has. Open the Springer address and update "
                 "find_supplement()."
                 % (len(reached), ", ".join(u[:60] for u, _ in reached)))
    print("  supplement: %s" % link[:110])

    try:
        blob = fetch(link, binary=True)
    except Exception as e:
        sys.exit("could not download the supplement: %s" % e)

    if link.lower().endswith((".xlsx", ".xls")):
        rows = rows_from_xlsx(blob)
    elif link.lower().endswith(".csv"):
        rows = rows_from_csv(blob.decode("utf-8", "replace"))
    else:
        sys.exit("supplement is %s, which this script cannot parse. Download it "
                 "by hand from %s and convert to CSV."
                 % (link.rsplit(".", 1)[-1], ARTICLE))

    print("  %d rows in the supplement" % len(rows))

    have = set()
    if HAND.exists():
        try:
            have = {r["name"].lower()
                    for r in json.loads(HAND.read_text(encoding="utf-8"))["projects"]}
        except Exception:
            pass

    out, skipped, nogeo = [], 0, 0
    for i, r in enumerate(rows):
        rec = to_record(r, i)
        if rec is None:
            nogeo += 1; continue
        if rec["name"].lower() in have:
            skipped += 1; continue
        out.append(rec)

    print("  usable: %d | already hand-written: %d | no country match: %d"
          % (len(out), skipped, nogeo))
    if nogeo:
        print("    (rows without a country this script can place are dropped "
              "rather than guessed at)")

    print()
    print("  Sources that exist and are NOT compiled here:")
    for name, url, note in EXTRA_SOURCES:
        print("    %-12s %s" % (name, url))
        if note:
            print("                 %s" % note)
    print("  Every record emitted carries the scope of its own source, because "
          "no single one of them is a world picture.")

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written")
        return
    OUT.write_text(json.dumps({
        "note": ("The GM Contamination Register 1997-2013, recovered from the "
                 "open-access supplementary data of Price & Cotter 2014 "
                 "(doi:10.1186/s40550-014-0005-8, CC BY). The Register was "
                 "compiled by GeneWatch UK and Greenpeace International and "
                 "stopped in 2013. Country-level positions only."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
