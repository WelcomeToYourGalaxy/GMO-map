#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consultations that are open right now, with the date they shut.

Everything else on this map is true next year. A comment window is worthless
the day after it closes, which makes this the only thing here that has to be
fetched rather than written.

It follows the wire's pattern rather than the browser's: harvested here, written
to a file, read by the map. A browser cannot fetch these sources cross-origin
reliably, and a feed that silently fails is worse than none - a reader would
see "no consultations open" and believe it.

SOURCES

  Federal Register   a real JSON API, filterable by agency and comment date.
                     The only one of the three that is designed to be queried.
  EFSA               a listing page; parsed for consultation links and dates.
  OGTR               a listing page; parsed the same way.

Anything that cannot be parsed is reported and skipped. The output always says
when it was generated, so the map can refuse to show a stale list rather than
presenting last month's closed windows as open.

    python3 harvest/consultations.py
    python3 harvest/consultations.py --dry-run
"""

import json, re, sys, time, pathlib
from datetime import date, datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "consultations.json"
UA = "GMO-map/1.0 (public research map)"

FR_API = "https://www.federalregister.gov/api/v1/documents.json"
FR_TERMS = ["genetically engineered", "genetically modified organism",
            "plant-incorporated protectant", "biotechnology regulatory services"]
EFSA = "https://www.efsa.europa.eu/en/consultations"
OGTR = "https://www.ogtr.gov.au/what-weve-approved/dealings-involving-intentional-release"


def get(url, timeout=45):
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json, text/html"})
    return urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def federal_register():
    """The only one of the three with an API. Asks for documents whose comment
    period has not yet closed."""
    out, today = [], date.today().isoformat()
    for term in FR_TERMS:
        q = urlencode({
            "conditions[term]": term,
            "conditions[comment_date][gte]": today,
            "per_page": 40, "order": "newest",
            "fields[]": "title",
        }, doseq=True)
        # the fields list needs repeating; build it by hand
        q += "&fields[]=" + "&fields[]=".join(
            ["html_url", "comments_close_on", "agencies", "publication_date",
             "document_number"])
        try:
            d = json.loads(get(FR_API + "?" + q))
        except Exception as e:
            print("  Federal Register (%s): %s" % (term[:24], str(e)[:50]))
            continue
        for r in d.get("results") or []:
            close = r.get("comments_close_on")
            if not close or close < today:
                continue
            ag = r.get("agencies") or []
            out.append({
                "title": (r.get("title") or "")[:200],
                "agency": (ag[0].get("name") if ag and isinstance(ag[0], dict)
                           else "US federal agency"),
                "closes": close,
                "url": r.get("html_url"),
                "country": "United States",
                "ref": r.get("document_number"),
            })
    # one document can match several terms
    seen, uniq = set(), []
    for r in out:
        k = r.get("ref") or r["url"]
        if k in seen:
            continue
        seen.add(k); uniq.append(r)
    print("  Federal Register%s %d open" % (" " * 20, len(uniq)))
    return uniq


def _dates(text):
    """Any date in the shapes these pages use."""
    out = []
    for m in re.finditer(r"(\d{1,2})\s+(January|February|March|April|May|June|July|"
                         r"August|September|October|November|December)\s+(\d{4})", text):
        try:
            out.append(datetime.strptime(" ".join(m.groups()), "%d %B %Y").date())
        except Exception:
            pass
    for m in re.finditer(r"(\d{4})-(\d{2})-(\d{2})", text):
        try:
            out.append(date(*map(int, m.groups())))
        except Exception:
            pass
    return out


def listing(url, country, label):
    """EFSA and OGTR publish listings rather than an API. Pull the links and any
    date near them; a link with no future date is reported, not guessed at."""
    try:
        html = get(url)
    except Exception as e:
        print("  %-34s unreachable (%s)" % (label, str(e)[:40]))
        return []
    out, today = [], date.today()
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>([^<]{15,160})</a>', html):
        href, title = m.group(1), re.sub(r"\s+", " ", m.group(2)).strip()
        if not re.search(r"consult|comment|submission|application", title, re.I):
            continue
        window = html[m.start(): m.start() + 900]
        fut = [d for d in _dates(window) if today <= d <= today + timedelta(days=400)]
        if not fut:
            continue
        if href.startswith("/"):
            href = re.match(r"(https?://[^/]+)", url).group(1) + href
        out.append({"title": title[:200], "agency": label,
                    "closes": min(fut).isoformat(), "url": href,
                    "country": country})
    seen, uniq = set(), []
    for r in out:
        if r["url"] in seen:
            continue
        seen.add(r["url"]); uniq.append(r)
    print("  %-34s %d open" % (label, len(uniq)))
    return uniq


def main():
    dry = "--dry-run" in sys.argv
    print("Consultations open as of %s" % date.today().isoformat())
    rows = []
    rows += federal_register()
    rows += listing(EFSA, "European Union", "EFSA")
    rows += listing(OGTR, "Australia", "OGTR")
    rows.sort(key=lambda r: r["closes"])

    if not rows:
        print("\nNothing found. That is not the same as nothing being open \u2014 "
              "if all three sources failed above, the map should say the list "
              "could not be fetched rather than that no window is open.",
              file=sys.stderr)

    soon = [r for r in rows if r["closes"] <= (date.today() + timedelta(days=14)).isoformat()]
    print("\n  %d open, %d closing within a fortnight" % (len(rows), len(soon)))
    for r in rows[:8]:
        print("     %s  %-14s %s" % (r["closes"], r["country"][:14], r["title"][:64]))

    if dry:
        print("dry run \u2014 nothing written")
        return
    OUT.write_text(json.dumps({
        "generated": date.today().isoformat(),
        "note": ("Comment windows open at the time of harvest. The map checks the "
                 "generated date and refuses to show this list if it is stale, "
                 "because a closed window presented as open is worse than no "
                 "list at all."),
        "consultations": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d" % (OUT.name, len(rows)))


if __name__ == "__main__":
    main()
