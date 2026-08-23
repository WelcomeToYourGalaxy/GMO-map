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
# A term search on the Federal Register is far too loose: "genetically
# engineered" matches any notice that mentions it in passing, and most of what
# came back was pesticide registration and chemical review with a single
# incidental sentence. Two changes fix it.
#
# First, phrases that only appear when an engineered ORGANISM is the subject.
# Second, a title test applied afterwards, because the API searches full text
# and a document about this subject says so in its title.
FR_TERMS = ["genetically engineered organism", "modified organism",
            "petition for determination of nonregulated status",
            "plant-incorporated protectant", "bioengineered food",
            "gene drive", "genetically engineered animal"]

# Applied to the title. A notice that passes the search and fails this is about
# something else that mentioned the subject once.
TITLE_OK = re.compile(
    r"genetic|engineered|bioengineer|nonregulated status|"
    r"plant-incorporated|gene drive|biotechnolog|transgenic|"
    r"modified organism", re.I)

# And notices that are about a chemical, which is a different subject even when
# the crop it is sprayed on is engineered.
TITLE_NO = re.compile(
    r"tolerances?\b|pesticide product registration|registration review|"
    r"inert ingredient|antimicrobial|residue|air quality|drinking water|"
    r"significant new use|premanufacture notice", re.I)
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
            title = r.get("title") or ""
            if not TITLE_OK.search(title) or TITLE_NO.search(title):
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
        if not TITLE_OK.search(title) or TITLE_NO.search(title):
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


# ============================================ GLOBAL COVERAGE ================
#
# Three sources gave three countries, and every entry sat under "Worldwide"
# because that is what a portal is. Two additions make this actually global,
# and both are databases of INDIVIDUAL notices with deadlines rather than pages
# to go and look at.
#
#   ePing / WTO TBT   Every WTO member must notify a draft technical regulation
#                     before enforcing it, with a comment period attached. That
#                     is 160-odd countries filing into one searchable database,
#                     and it is frequently the earliest public sight of a rule -
#                     including from countries whose own consultation pages are
#                     decorative. Guide 2 calls it the one hardly anybody uses.
#
#   BCH consultations The Cartagena Protocol requires a party to consult the
#                     public before most first release decisions, and the
#                     Clearing-House carries those records.
#
# Each notice carries the notifying country, so the panel can group by country
# instead of filing everything under Worldwide.

EPING = "https://eping.wto.org/en/Search/IndexSearch"
EPING_API = "https://epingalert.org/api/notifications"
BCH_API = ("https://api.cbd.int/api/v2013/index?q=%2A%3A%2A"
           "&fq=schema_s%3AbiosafetyDecision&rows=200&wt=json")

GM_TERMS = re.compile(
    r"genetic|engineered|bioengineer|transgenic|modified organism|"
    r"living modified|biosafety|gene drive|new genomic|biotech", re.I)


def eping():
    """WTO technical regulation notifications, filtered to this subject.

    The value here is coverage rather than depth: a notification from Kenya or
    Peru or Viet Nam appears in the same database as one from the EU, with the
    same fields and the same deadline, which no national portal gives.
    """
    out = []
    for url in (EPING_API + "?keyword=genetically+modified&limit=100",
                EPING_API + "?keyword=biosafety&limit=100"):
        kw = url.split("keyword=")[1].split("&")[0]
        try:
            d = json.loads(get(url))
        except Exception as e:
            # `return` here abandoned the SECOND keyword as well, so one bad
            # response lost the whole source rather than half of it. And the
            # message did not say WHICH keyword failed, which is the thing
            # needed to tell a dead endpoint from an empty result - the
            # difference between "fix the URL" and "the search found nothing".
            print("  %-34s %s  [%s]" % ("ePing / WTO TBT", str(e)[:44], kw))
            continue
        rows = d if isinstance(d, list) else (d.get("results") or d.get("data") or [])
        if not rows:
            # Reached the server and got an empty or unrecognised body. Said
            # plainly, because it looks identical to a failure in the output
            # file and is a different problem: either the query matched nothing
            # or the response shape changed under the two keys read above.
            print("  %-34s reachable, 0 rows  [%s]" % ("ePing / WTO TBT", kw))
        for r in rows:
            title = str(r.get("title") or r.get("productCovered") or "")
            if not GM_TERMS.search(title):
                continue
            close = str(r.get("commentDeadline") or r.get("finalDateForComments") or "")[:10]
            if not close or close < date.today().isoformat():
                continue
            out.append({"title": title[:200],
                        "agency": "WTO TBT notification",
                        "closes": close,
                        "url": r.get("url") or EPING,
                        "country": str(r.get("notifyingMember")
                                       or r.get("member") or "").strip() or "Worldwide",
                        "ref": r.get("symbol") or r.get("id")})
    seen, uniq = set(), []
    for r in out:
        k = r.get("ref") or r["url"] + r["title"][:40]
        if k in seen:
            continue
        seen.add(k); uniq.append(r)
    print("  %-34s %d open" % ("ePing / WTO TBT", len(uniq)))
    return uniq


def bch_consultations():
    """Decisions filed to the Clearing-House that are still open for comment."""
    try:
        d = json.loads(get(BCH_API))
    except Exception as e:
        print("  %-34s %s" % ("Biosafety Clearing-House", str(e)[:44]))
        return []
    docs = (d.get("response") or d).get("docs") or []
    out, today = [], date.today().isoformat()
    for doc in docs:
        title = str(doc.get("title_EN_s") or doc.get("title_s") or "")
        if not title:
            continue
        # the country is a prefix on the grouping field, not a field of its own
        gov = ""
        v = doc.get("grp_government_schema_s")
        if isinstance(v, list):
            v = v[0] if v else ""
        if v and "_" in str(v):
            gov = str(v).split("_", 1)[0].upper()
        close = str(doc.get("commentDeadline_dt") or doc.get("deadline_dt") or "")[:10]
        if not close or close < today:
            continue
        out.append({"title": title[:200], "agency": "Biosafety Clearing-House",
                    "closes": close, "url": "https://bch.cbd.int/",
                    "country": gov or "Worldwide"})
    print("  %-34s %d open" % ("Biosafety Clearing-House", len(out)))
    return out


def main():
    dry = "--dry-run" in sys.argv
    print("Consultations open as of %s" % date.today().isoformat())
    rows = []
    rows += federal_register()
    rows += listing(EFSA, "European Union", "EFSA")
    rows += listing(OGTR, "Australia", "OGTR")
    rows += eping()
    rows += bch_consultations()
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
