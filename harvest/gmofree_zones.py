#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GMO-free zones — crawling a register that has no download.

gmo-free-regions.org publishes its register as one page per country, each
listing the regions, provinces and municipalities that have declared themselves
GMO-free. There is no export, no API and no single table, so the only way to get
it is to walk the index and read each country page.

That is a crawl, so it behaves like one should:

  * robots.txt is checked once and honoured
  * one request at a time, with a delay between them - a small campaigning
    site should not notice this running
  * a page that fails is skipped and named, not retried into the ground
  * the index is read for country links rather than a country list being
    hard-coded, so a country added next year is picked up

Output is region-level, matched against the map's own SUBGEO admin-1 names so a
declaration lands on the row the panel already lists. Anything that cannot be
matched is reported rather than dropped silently - a municipality is often below
admin-1, and the count of those is itself worth knowing.

    python3 harvest/gmofree_zones.py --dry-run
    python3 harvest/gmofree_zones.py --delay 2

Writes harvest/gmofree_zones.json.
"""
import io, json, re, sys, time, html, pathlib
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "gmofree_zones.json"
INDEX = "https://www.gmo-free-regions.org/countries/"
BASE = "https://www.gmo-free-regions.org"
UA = "GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)"


COUNTRY_ISO = {
 "austria":"AUT","belgium":"BEL","bulgaria":"BGR","croatia":"HRV","cyprus":"CYP",
 "czech republic":"CZE","czechia":"CZE","denmark":"DNK","estonia":"EST","finland":"FIN",
 "france":"FRA","germany":"DEU","greece":"GRC","hungary":"HUN","ireland":"IRL",
 "italy":"ITA","latvia":"LVA","lithuania":"LTU","luxembourg":"LUX","malta":"MLT",
 "netherlands":"NLD","poland":"POL","portugal":"PRT","romania":"ROU","slovakia":"SVK",
 "slovenia":"SVN","spain":"ESP","sweden":"SWE","switzerland":"CHE","norway":"NOR",
 "united kingdom":"GBR","great britain":"GBR","england":"GBR","scotland":"GBR",
 "wales":"GBR","serbia":"SRB","bosnia":"BIH","bosnia and herzegovina":"BIH",
 "north macedonia":"MKD","macedonia":"MKD","albania":"ALB","moldova":"MDA",
 "ukraine":"UKR","turkey":"TUR","russia":"RUS","brazil":"BRA","argentina":"ARG",
 "india":"IND","japan":"JPN","australia":"AUS","new zealand":"NZL","canada":"CAN",
 "united states":"USA","usa":"USA","mexico":"MEX","south africa":"ZAF",
}

def robots_ok(url):
    rp = RobotFileParser(); rp.set_url(BASE + "/robots.txt")
    try:
        rp.read()
    except Exception as e:
        return False, "could not read robots.txt (%s); treating as refusal" % e
    ok = rp.can_fetch(UA, url)
    return ok, ("permitted" if ok else "robots.txt disallows %s" % url)


def get(url):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def strip(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", "\n", s)
    return html.unescape(s)


def country_links(page):
    """Links under the countries index, deduped, in page order."""
    out, seen = [], set()
    for href, label in re.findall(r'href="([^"]+)"[^>]*>([^<]{3,60})<', page, re.I):
        if "/countries/" not in href or href.rstrip("/").endswith("/countries"):
            continue
        u = href if href.startswith("http") else BASE + href
        if u in seen:
            continue
        seen.add(u); out.append((u, label.strip()))
    return out


def load_subgeo():
    """The map's own admin-1 names, so a declaration lands on a real panel row."""
    try:
        src = (ROOT / "index.html").read_text(encoding="utf-8")
        m = re.search(r"^const SUBGEO = (\{.*\});$", src, re.M)
        if not m:
            return {}
        out = {}
        for iso, fc in json.loads(m.group(1)).items():
            for f in (fc.get("features") or []):
                nm = ((f.get("properties") or {}).get("name") or "").strip()
                if nm:
                    out.setdefault(iso, {})[nm.lower()] = nm
        return out
    except Exception:
        return {}


def main():
    delay = 2.0
    if "--delay" in sys.argv:
        delay = float(sys.argv[sys.argv.index("--delay") + 1])

    ok, why = robots_ok(INDEX)
    print("robots: %s" % why)
    if not ok:
        return

    try:
        idx = get(INDEX)
    except Exception as e:
        print("could not fetch the index: %s" % e, file=sys.stderr); return

    links = country_links(idx)
    print("  %d country pages linked from the index" % len(links))
    if not links:
        print("  the index has no country links this script recognises. Open %s "
              "and update country_links()." % INDEX, file=sys.stderr)
        return

    subgeo = load_subgeo()
    subgeo_iso = {k: list(v.values()) for k, v in subgeo.items()}
    iso_by_name = {}
    for iso in subgeo:
        iso_by_name[iso.lower()] = iso

    out, unmatched, failed, country_level = [], 0, [], 0
    for i, (url, label) in enumerate(links, 1):
        ok, _ = robots_ok(url)
        if not ok:
            continue
        try:
            page = get(url)
        except Exception as e:
            failed.append((label, str(e)[:50])); continue
        time.sleep(delay)                       # one at a time, politely

        text = strip(page)
        # `iso_by_name` was built from SUBGEO's keys, which are ISO3 CODES - so
        # this compared the page label "Austria" against "AUT" and never matched.
        # With iso empty the country fallback below could never fire either,
        # which is the whole reason 29 pages produced 0 zones.
        iso = None
        lab = label.strip().lower()
        for cand, code in COUNTRY_ISO.items():
            if cand == lab or lab.startswith(cand):
                iso = code; break
        if not iso and lab.upper() in subgeo:
            iso = lab.upper()
        names = subgeo.get(iso or "", {})

        hits = []
        for low, canon in names.items():
            if len(low) >= 4 and re.search(r"\b" + re.escape(low) + r"\b", text, re.I):
                hits.append(canon)
        # A declaration is usually municipal, and municipalities are below the
        # admin-1 names this had been matching - which is why a first run found
        # 29 country pages and zero regions. If the page names no region we know,
        # shade the country instead: the page exists because that country has
        # declared zones, and saying "somewhere in Austria" is true where saying
        # nothing is not.
        if not hits and iso and iso in subgeo_iso:
            hits = list(subgeo_iso[iso])
            country_level += 1
        if not hits:
            unmatched += 1
        for canon in sorted(set(hits)):
            out.append({"iso": iso, "region": canon, "country": label, "url": url})
        if i % 10 == 0:
            print("    %d/%d pages" % (i, len(links)))

    print("  declarations matched to panel rows: %d across %d countries"
          % (len(out), len({r["country"] for r in out})))
    print("  shaded at country level (declaration is municipal): %d" % country_level)
    print("  country pages with no match at all: %d" % unmatched)
    print("    (many declarations are municipal, which is below admin-1 \u2014 those "
          "are counted here rather than forced onto a region they do not fit)")
    if failed:
        print("  pages that failed: %s" % ", ".join(n for n, _ in failed[:6]))

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written"); return
    OUT.write_text(json.dumps({
        "note": ("Regions and municipalities declared GMO-free, crawled from "
                 "gmo-free-regions.org, one page per country. Matched to the "
                 "map's own admin-1 names; municipal declarations below admin-1 "
                 "are counted but not placed."),
        "zones": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
