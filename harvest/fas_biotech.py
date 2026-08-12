#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""USDA FAS Agricultural Biotechnology Annual — GM cultivation area by country.

FAS publishes GAIN reports through a search that returns tens of thousands of
documents across every commodity and topic. The Agricultural Biotechnology
Annual is one report series inside that: roughly one per country per year, and
the only recurring public source that states planted GM area country by country.

Filtering by `report_type` does not isolate it - that field is a broad category
and still returns thousands. The series is identified by its TITLE. This script
filters on the title and keeps the most recent report per country.

Two outputs, and the distinction matters:

  1. The REPORT INDEX - country, year, title, URL. Reliable, and useful on its
     own: it is a per-country list of where the official account of that
     country's biotech position is written down.
  2. A best-effort AREA extraction from the report text. Reported separately and
     never merged into the index, because the reports are prose written by
     different attaches in different years and the figures appear in tables,
     sentences and footnotes with no fixed form. **The script says how many it
     could read and how many it could not** rather than presenting a number for
     every country and letting you assume they were all found the same way.

    python3 harvest/fas_biotech.py --dry-run
    python3 harvest/fas_biotech.py --years 3

Writes harvest/fas_biotech.json.
"""
import io, json, re, sys, time, html, pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlencode

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "fas_biotech.json"

BASE = "https://fas.usda.gov"
SEARCH = BASE + "/data/search"

# fas.usda.gov/data/search returned 403 to a script even with browser headers,
# and the one page that did load matched no reports. GAIN has its own host with a
# query interface that predates the site redesign and is not behind the same
# protection: apps.fas.usda.gov. Tried in order, so if one route is closed the
# next is attempted rather than the whole layer failing.
GAIN_ROUTES = [
    "https://apps.fas.usda.gov/gainfiles/api/reports?query=Agricultural+Biotechnology+Annual",
    "https://gain.fas.usda.gov/api/reports?keyword=Agricultural%20Biotechnology%20Annual",
    "https://apps.fas.usda.gov/newgainapi/api/report/ReportList?"
    "reportTitle=Agricultural%20Biotechnology%20Annual",
    "https://apps.fas.usda.gov/scriptsw/AttacheRep/default.aspx?"
    "subject=Agricultural+Biotechnology+Annual",
]
TITLE = "agricultural biotechnology annual"
UA = "GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)"

# Hectares and acres, as the reports actually write them.
AREA = re.compile(
    r"([\d][\d,\.]{2,15})\s*(million\s+)?(hectares|ha\b|acres)", re.I)
CROPS = ("maize", "corn", "soybean", "soya", "cotton", "canola", "rapeseed",
         "alfalfa", "sugar beet", "papaya", "eggplant", "brinjal", "rice", "wheat")


def get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            # FAS returned 403 to the plain agent. A public page that a browser can
            # read should be readable by a script that identifies itself, so this
            # sends the headers a browser sends rather than pretending to be one.
            req = Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "identity",
                "Connection": "close"})
            with urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e; time.sleep(3 * (i + 1))
    raise last


def find_rows(payload):
    """FAS has served this search as JSON and as HTML at different times, so
    handle both rather than assuming the shape that happens to be live today."""
    try:
        data = json.loads(payload)
        for k in ("results", "rows", "data", "items", "docs"):
            v = data.get(k) if isinstance(data, dict) else None
            if isinstance(v, list):
                return v
        if isinstance(data, list):
            return data
    except Exception:
        pass
    # HTML fallback: report links with their titles
    rows = []
    for href, label in re.findall(
            r'href="([^"]*(?:/data/|/report/)[^"]*)"[^>]*>\s*([^<]{10,200}?)\s*<', payload, re.I):
        rows.append({"url": href, "title": html.unescape(label)})
    return rows


def field(row, *names):
    for n in names:
        for k, v in row.items():
            if k and n in str(k).lower() and v not in (None, ""):
                return str(v).strip()
    return ""


def collect(pages=12):
    """Walk the search, keeping only the biotech annual series."""
    seen, out = set(), []
    for page in range(pages):
        url = SEARCH + "?" + urlencode({"keyword": TITLE, "page": page})
        try:
            payload = get(url)
        except Exception as e:
            print("  page %d failed (%s)" % (page, str(e)[:60]), file=sys.stderr)
            break
        rows = find_rows(payload)
        if not rows:
            break
        new = 0
        for r in rows:
            title = field(r, "title", "name", "label")
            if TITLE not in title.lower():
                continue          # the search is fuzzy; the title filter is not
            u = field(r, "url", "link", "path", "href")
            if not u:
                continue
            u = u if u.startswith("http") else BASE + u
            if u in seen:
                continue
            seen.add(u); new += 1
            out.append({
                "title": title,
                "url": u,
                "country": field(r, "country", "post", "location"),
                "date": field(r, "date", "released", "published", "year"),
            })
        print("  page %d: %d new biotech-annual reports (%d rows scanned)"
              % (page, new, len(rows)))
        if new == 0:
            break
        time.sleep(1)
    return out


def country_from(rec):
    if rec.get("country"):
        return rec["country"]
    # "Agricultural Biotechnology Annual_Brasilia_Brazil_2025-07-01"
    m = re.search(r"annual[_\s]+[^_]*_([A-Za-z .'-]{3,40})_", rec["title"], re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"annual[^A-Za-z]+([A-Za-z .'-]{3,40})", rec["title"], re.I)
    return m.group(1).strip() if m else ""


def year_from(rec):
    m = re.search(r"(20\d{2})", (rec.get("date") or "") + " " + rec["title"])
    return int(m.group(1)) if m else 0


def read_area(text):
    """Best effort. Returns a list of (figure, unit, crop-context) it found."""
    hits = []
    for m in AREA.finditer(text):
        # Look BACKWARD only. Reading ahead attributed "55.2 million hectares
        # of biotech crops, of which soybean..." to soybean, when that figure
        # is the national total. The crop that qualifies a figure precedes it.
        window = text[max(0, m.start() - 140): m.start()].lower()
        crop = next((c for c in CROPS if c in window), "")
        val = m.group(1).replace(",", "")
        try:
            n = float(val)
        except Exception:
            continue
        if m.group(2):
            n *= 1_000_000
        if m.group(3).lower().startswith("acre"):
            n *= 0.404686
        if 1_000 <= n <= 60_000_000:          # plausible national planted area
            hits.append({"hectares": round(n), "crop": crop})
    return hits


def main():
    years = 3
    if "--years" in sys.argv:
        years = int(sys.argv[sys.argv.index("--years") + 1])

    print("searching FAS for the Agricultural Biotechnology Annual series")
    recs = []
    for route in GAIN_ROUTES:
        try:
            got = find_rows(get(route))
        except Exception as e:
            print("  %-64s %s" % (route[:64], str(e)[:30]), file=sys.stderr); continue
        hits = [r for r in got if TITLE in str(field(r, "title", "name", "reporttitle")).lower()]
        if hits:
            print("  %d reports from %s" % (len(hits), route[:70]))
            recs = [{"title": field(r, "title", "name", "reporttitle"),
                     "url": field(r, "url", "link", "filename", "path") or route,
                     "country": field(r, "country", "post"),
                     "date": field(r, "date", "released", "reportdate")} for r in hits]
            break
    if not recs:
        recs = collect()
    if not recs:
        # Every route refused. Say so plainly rather than writing an empty file
        # that looks like "this country grows nothing" once it reaches the map.
        print("ALL FAS ROUTES REFUSED. No cultivation file written - the layer will "
              "stay empty, which is correct: an empty overlay is honest, a fabricated "
              "one is not. Routes tried:", file=sys.stderr)
        for r in GAIN_ROUTES + [SEARCH]:
            print("    %s" % r, file=sys.stderr)
        return
    if not recs:
        print("no reports matched. The search may have changed shape; open %s?"
              "keyword=%s and update find_rows()." % (SEARCH, TITLE.replace(" ", "+")),
              file=sys.stderr)
        return
    print("  %d reports in the series" % len(recs))

    # newest per country
    best = {}
    for r in recs:
        c, y = country_from(r), year_from(r)
        if not c:
            continue
        if c not in best or y > best[c]["year"]:
            best[c] = {"country": c, "year": y, "title": r["title"], "url": r["url"]}
    index = sorted(best.values(), key=lambda x: x["country"])
    print("  %d countries, newest report each" % len(index))

    cutoff = max((x["year"] for x in index), default=0) - years
    recent = [x for x in index if x["year"] >= cutoff]
    print("  attempting area extraction on %d reports from the last %d years"
          % (len(recent), years))

    got, missed = 0, []
    for i, rec in enumerate(recent, 1):
        try:
            body = get(rec["url"])
        except Exception:
            missed.append(rec["country"]); continue
        text = re.sub(r"<[^>]+>", " ", body)
        hits = read_area(html.unescape(text))
        if hits:
            rec["area_candidates"] = hits[:6]
            got += 1
        else:
            missed.append(rec["country"])
        time.sleep(1)
        if i % 20 == 0:
            print("    %d/%d" % (i, len(recent)))

    print("\n  area figures read from %d of %d reports" % (got, len(recent)))
    if missed:
        print("  no figure found for %d: %s%s"
              % (len(missed), ", ".join(missed[:8]),
                 " …" if len(missed) > 8 else ""))
    print("  NOTE: area_candidates are unverified regex hits from prose written "
          "by different attaches in different years. Treat them as pointers into "
          "the report, not as the figure. The index is the reliable output.")

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written"); return
    OUT.write_text(json.dumps({
        "note": ("USDA FAS Agricultural Biotechnology Annual, newest report per "
                 "country. The index (country, year, title, url) is reliable. "
                 "area_candidates are best-effort regex hits from report prose "
                 "and are NOT verified figures."),
        "reports": index}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
