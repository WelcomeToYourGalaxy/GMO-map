#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Event approvals by country, from the ISAAA GM Approval Database.

WHY THIS INSTEAD OF THREE MORE NATIONAL HARVESTERS. India, China and New
Zealand were the remaining gaps, and each would have been its own scraper
against its own page layout. ISAAA already holds all three, and everywhere
else, behind one URL pattern:

    /gmapprovaldatabase/approvedeventsin/default.asp?CountryID=IN

One harvester, every country. India shows 11 approved events, New Zealand 127 -
which is itself worth seeing, because New Zealand permits almost no cultivation
and those 127 are import and food approvals. The distinction between what a
country lets in and what it lets be grown is exactly what a single national
number hides.

WHOSE DATABASE THIS IS, which the map should say rather than imply. ISAAA is
the International Service for the Acquisition of Agri-biotech Applications. It
exists to promote the adoption of agricultural biotechnology, it is funded in
part by the companies whose products it counts, and this database is one of its
advocacy outputs. That does not make the counts wrong - they are compiled from
decision documents, Clearing-House filings and published papers, and they are
checkable against those. It does mean the framing is not neutral, and that
every record here is tagged with its source so a reader can weigh it.

WHAT IT WILL NOT DO. It will not present these as this map's own finding, and
it will not merge them silently with the national registers. An ISAAA count and
a CTNBio count of the same country can differ, and where they do, the
difference is information rather than an error to be smoothed away.

    python3 harvest/isaaa_approvals.py
    python3 harvest/isaaa_approvals.py --selftest      # no network
"""

import json, re, sys, time, pathlib
from urllib.request import Request, urlopen

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "isaaa_approvals.json"
UA = "GMO-map/1.0 (public research map)"
BASE = ("https://www.isaaa.org/gmapprovaldatabase/approvedeventsin/"
        "default.asp?CountryID=%s")

# ISO2 to the name this map uses, so records land on the countries that exist
# in resources.json rather than under a code.
COUNTRIES = {
    "IN": "India", "CN": "China", "NZ": "New Zealand", "JP": "Japan",
    "KR": "Republic of Korea", "TW": "Taiwan", "PH": "Philippines",
    "VN": "Vietnam", "TH": "Thailand", "MY": "Malaysia", "ID": "Indonesia",
    "BD": "Bangladesh", "PK": "Pakistan", "MM": "Myanmar",
    "AU": "Australia", "CA": "Canada", "US": "United States",
    "BR": "Brazil", "AR": "Argentina", "PY": "Paraguay", "UY": "Uruguay",
    "BO": "Bolivia", "CL": "Chile", "CO": "Colombia", "CR": "Costa Rica",
    "HN": "Honduras", "MX": "Mexico", "PA": "Panama",
    "ZA": "South Africa", "NG": "Nigeria", "KE": "Kenya", "GH": "Ghana",
    "EG": "Egypt", "SD": "Sudan", "MW": "Malawi", "ET": "Ethiopia",
    "BF": "Burkina Faso", "SZ": "Eswatini", "MZ": "Mozambique",
    "EU": "European Union", "RU": "Russia", "TR": "Turkey", "UA": "Ukraine",
    "IL": "Israel", "NO": "Norway", "CH": "Switzerland", "SG": "Singapore",
}

TOTAL_RE = re.compile(r"Total:\s*(\d+)\s*events?\s*approved", re.I)
# Event codes as ISAAA prints them, including the slashed-O form.
CODE_RE = re.compile(r"\b([A-Z]{2,4})[\s\-]?([0-9\u00d8O]{3,7})[\s\-]?([0-9])\b")


def norm_id(code):
    """Must agree with bch_organisms.norm and latam_approvals.norm_id. Three
    files now share this; if one drifts, cross-register lookups miss silently
    and a miss reads as the event not existing."""
    if not code:
        return ""
    s = str(code).upper()
    s = re.sub(r"[^A-Z0-9\u00d8\u00f8]", "", s)
    s = s.replace("\u00d8", "0").replace("\u00f8", "0")
    s = re.sub(r"(?<=[0-9])O", "0", s)
    s = re.sub(r"O(?=[0-9])", "0", s)
    return s


def get(url, timeout=45):
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    return urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def parse(country, html):
    """The declared total, and the event codes on the page.

    The total is read from the page's own wording rather than counted from
    rows: a table that fails to parse would otherwise report zero events, which
    is indistinguishable from a country having none.
    """
    m = TOTAL_RE.search(html)
    declared = int(m.group(1)) if m else None
    codes, seen = [], set()
    for cm in CODE_RE.finditer(html.upper()):
        code = "-".join(cm.groups())
        k = norm_id(code)
        if k and k not in seen:
            seen.add(k)
            codes.append({"id": code, "id_key": k})
    return {"country": country, "declared_total": declared,
            "events_parsed": len(codes), "events": codes}


def harvest():
    rows, missing = [], []
    for iso, name in sorted(COUNTRIES.items(), key=lambda t: t[1]):
        try:
            html = get(BASE % iso)
        except Exception as e:
            print("  %-22s %s" % (name, str(e)[:44]))
            missing.append(name)
            continue
        r = parse(name, html)
        rows.append(r)
        flag = ""
        # A gap between the declared total and what parsed is worth printing,
        # not smoothing: it means the page changed shape.
        if r["declared_total"] is not None and r["events_parsed"] < r["declared_total"]:
            flag = "   <- parsed fewer than declared"
        print("  %-22s declared %-5s parsed %-5d%s"
              % (name, r["declared_total"], r["events_parsed"], flag))
        time.sleep(0.5)

    if not rows:
        print("\nNothing fetched. Every country page uses the same URL pattern, "
              "so a total failure is the host refusing rather than the pages "
              "moving.", file=sys.stderr)
        return

    tot = sum(r["declared_total"] or 0 for r in rows)
    print("\n  %d countries, %d events declared in total" % (len(rows), tot))
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "source": "ISAAA GM Approval Database",
        "note": ("Compiled by ISAAA, which exists to promote agricultural "
                 "biotechnology and is funded in part by the companies whose "
                 "products it counts. The underlying decision documents are "
                 "public and checkable; the framing is not neutral. Counts here "
                 "are not merged with the national registers, because where the "
                 "two differ the difference is information."),
        "unreachable": missing,
        "countries": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


def selftest():
    ok = True

    def check(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %-50s %s" % (label, "pass" if good else
                              "FAIL got %r want %r" % (got, want)))

    check("id key agrees with the other two harvesters",
          norm_id("MON-877\u00d81-2"), "MON877012")
    check("plain-O spelling gives the same key",
          norm_id("MON-87701-2"), "MON877012")

    html = ("<p>Total: 3 events approved</p><table>"
            "<tr><td>MON-877\u00d81-2</td></tr><tr><td>DAS-59122-7</td></tr>"
            "<tr><td>MON-87701-2</td></tr></table>")
    r = parse("India", html)
    check("declared total read from the page's own wording",
          r["declared_total"], 3)
    check("duplicate spellings of one event folded", r["events_parsed"], 2)
    check("keys normalised", r["events"][0]["id_key"], "MON877012")

    r2 = parse("Nowhere", "<p>no table here</p>")
    check("no total found reports None, not zero", r2["declared_total"], None)
    check("no events reports zero parsed", r2["events_parsed"], 0)
    print("\n%s" % ("all pass" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    harvest()
