#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harvest the wire feeds into wire.json.

Reads the WIRE_FEEDS array straight out of index.html so the feed list lives in
exactly one place. Writes a flat array of items in the shape the map expects:

    {name, title, link, date (ISO8601), snippet, iso, region, lang, sig}

`iso` and `region` are left empty here; index.html geo-tags items at render time
from the headline text, and doing it once there beats doing it twice.

Usage:  python3 harvest/wire_harvest.py
"""
import json, re, sys, html, hashlib, pathlib
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from email.utils import parsedate_to_datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
OUT = ROOT / "wire.json"

KEEP_DAYS = 120          # how far back the archive is retained
MAX_ITEMS = 4000         # hard cap on file size
TIMEOUT = 25
UA = "Mozilla/5.0 (compatible; GMO-map wire harvester; +https://github.com/WelcomeToYourGalaxy/GMO-map)"


def feeds_from_index():
    """Pull WIRE_FEEDS = [[name, url], ...] out of index.html."""
    src = INDEX.read_text(encoding="utf-8")
    m = re.search(r"const WIRE_FEEDS\s*=\s*(\[.*?\]);", src, re.S)
    if not m:
        sys.exit("WIRE_FEEDS not found in index.html")
    return json.loads(m.group(1))


def fetch(url):
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
    with urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def strip(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        d = parsedate_to_datetime(s)
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            d = datetime.strptime(s[:len(fmt) + 6], fmt)
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return None


def tag(block, *names):
    for n in names:
        m = re.search(r"<%s[^>]*>(.*?)</%s>" % (n, n), block, re.S | re.I)
        if m:
            return m.group(1)
        m = re.search(r'<%s[^>]*href=["\']([^"\']+)["\']' % n, block, re.I)   # atom <link href>
        if m:
            return m.group(1)
    return ""


def parse_feed(name, xml):
    out = []
    blocks = re.findall(r"<item[\s>].*?</item>", xml, re.S | re.I) or \
             re.findall(r"<entry[\s>].*?</entry>", xml, re.S | re.I)
    for b in blocks:
        title = strip(tag(b, "title"))
        link = strip(tag(b, "link", "id"))
        if not title or not link:
            continue
        d = parse_date(strip(tag(b, "pubDate", "published", "updated", "dc:date")))
        if d is None:
            d = datetime.now(timezone.utc)
        out.append({
            "name": name,
            "title": title[:400],
            "link": link,
            "date": d.astimezone(timezone.utc).isoformat(),
            "snippet": strip(tag(b, "description", "summary", "content"))[:500],
            "iso": "", "region": "", "lang": "en", "sig": 0,
        })
    return out


def one(entry):
    name, url = entry[0], entry[1]
    try:
        return parse_feed(name, fetch(url))
    except (URLError, HTTPError, TimeoutError, OSError) as e:
        print("  ! %-42s %s" % (name, e), file=sys.stderr)
        return []


def main():
    feeds = feeds_from_index()
    print("harvesting %d feeds" % len(feeds))
    items = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for got in ex.map(one, feeds):
            items.extend(got)
    print("  fetched %d items" % len(items))

    # merge with what is already on disk so a transient feed outage never
    # silently truncates the archive
    if OUT.exists():
        try:
            items.extend(json.loads(OUT.read_text(encoding="utf-8")) or [])
        except Exception:
            pass

    seen, merged = set(), []
    cutoff = datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)
    for it in items:
        key = hashlib.sha1((it.get("link") or it.get("title", "")).encode("utf-8")).hexdigest()
        if key in seen:
            continue
        d = parse_date(it.get("date"))
        if d and d < cutoff:
            continue
        seen.add(key)
        merged.append(it)

    merged.sort(key=lambda x: x.get("date", ""), reverse=True)
    merged = merged[:MAX_ITEMS]
    OUT.write_text(json.dumps(merged, ensure_ascii=False), encoding="utf-8")
    print("wrote %s: %d items" % (OUT.name, len(merged)))


if __name__ == "__main__":
    main()
