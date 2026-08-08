#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Release decisions from every Cartagena party, not just the United States.

The map's release layer has been overwhelmingly American for one reason: APHIS
publishes a bulk CSV and almost nobody else does. That is a fact about
publishing, not about where the industry operates, and left uncorrected it makes
the United States look like the whole story.

The Biosafety Clearing-House is the correction. Under Article 20 of the Cartagena
Protocol every party files its decisions there \u2014 environmental releases including
field trials, and domestic-use decisions on organisms that may cross a border \u2014
within 15 days of taking them. 173 parties. It is free, public, and it is the
only place national release decisions from that many countries sit together.

    python3 harvest/bch_decisions.py --dry-run
    python3 harvest/bch_decisions.py

Writes harvest/bch_decisions.json, merged into projects.json.

WHAT THIS WILL NOT FIX
The United States is not a party to the Protocol and files nothing here. So the
two sources are complementary rather than overlapping: APHIS for the US, BCH for
everywhere else. Countries that joined late, or that file irregularly, will still
be thin - and a country with no records here has not necessarily approved
nothing. It may simply not have filed.
"""
import io, json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlencode

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "bch_decisions.json"

BASE = "https://bch.cbd.int"
# The BCH front end does not serve its own data. It reads a Solr index behind
# the Secretariat's shared API at api.cbd.int, documented in scbd/scbd.github.io
# as "GET /api/v2013/index - Load information from solr index". The earlier
# attempts here failed because they asked bch.cbd.int for records it does not
# hold: 401 on one path, 404 on another, timeout on a third.
API = "https://api.cbd.int/api/v2013/index"
UA = "GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)"

# The record types that describe a release or a placing on the market.
SCHEMAS = ("decision", "biosafetydecision", "dcs")

# Country centroids for the parties that file most often. A decision is national
# in scope, so a centroid is the honest position - there is no site to place.
C = {
 "AR":(-34.6,-58.4),"AT":(47.5,14.6),"AU":(-25.3,133.8),"BD":(23.7,90.4),"BE":(50.5,4.5),
 "BF":(12.2,-1.6),"BO":(-16.3,-63.6),"BR":(-14.2,-51.9),"BG":(42.7,25.5),"CA":(56.1,-106.3),
 "CH":(46.8,8.2),"CL":(-35.7,-71.5),"CN":(35.9,104.2),"CO":(4.6,-74.3),"CR":(9.7,-83.8),
 "CU":(21.5,-79.5),"CZ":(49.8,15.5),"DE":(51.2,10.5),"DK":(56.3,9.5),"EC":(-1.8,-78.2),
 "EG":(26.8,30.8),"ES":(40.5,-3.7),"ET":(9.1,40.5),"EU":(50.8,4.4),"FI":(61.9,25.7),
 "FR":(46.2,2.2),"GB":(55.4,-3.4),"GH":(7.9,-1.0),"GR":(39.1,21.8),"HU":(47.2,19.5),
 "ID":(-0.8,113.9),"IN":(20.6,79.0),"IR":(32.4,53.7),"IT":(41.9,12.6),"JP":(36.2,138.3),
 "KE":(-0.02,37.9),"KR":(35.9,127.8),"LK":(7.9,80.8),"MW":(-13.3,34.3),"MX":(23.6,-102.6),
 "MY":(4.2,102.0),"NG":(9.1,8.7),"NL":(52.1,5.3),"NO":(60.5,8.5),"NZ":(-40.9,174.9),
 "PE":(-9.2,-75.0),"PH":(12.9,121.8),"PK":(30.4,69.3),"PL":(51.9,19.1),"PT":(39.4,-8.2),
 "PY":(-23.4,-58.4),"RO":(45.9,25.0),"RU":(61.5,105.3),"SD":(12.9,30.2),"SE":(60.1,18.6),
 "SK":(48.7,19.7),"SZ":(-26.5,31.5),"TH":(15.9,101.0),"TR":(39.0,35.2),"TZ":(-6.4,34.9),
 "UA":(48.4,31.2),"UG":(1.4,32.3),"UY":(-32.5,-55.8),"VN":(14.1,108.3),"ZA":(-30.6,22.9),
 "ZM":(-13.1,27.8),"ZW":(-19.0,29.2),
}


def get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = Request(url, headers={"User-Agent": UA,
                                        "Accept": "application/json, application/rss+xml, text/html;q=0.8"})
            with urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e; time.sleep(3 * (i + 1))
    raise last


def endpoints():
    """Solr queries against the shared CBD index, then the old guesses as a
    fallback. `schema_s` names the record type; the BCH decision schemas differ
    slightly by era, so several are tried."""
    q = []
    for schema in ("biosafetyDecision", "decision", "nationalDecision"):
        q.append(API + "?" + urlencode({
            "q": "*:*", "fq": "schema_s:" + schema, "rows": 2000,
            "wt": "json", "sort": "createdDate_dt desc"}))
    q.append(API + "?" + urlencode({
        "q": "biosafety decision release", "rows": 2000, "wt": "json"}))
    return q + [
        BASE + "/api/v2013/documents?schema=decision&format=json",
        BASE + "/rss/decisions.aspx",
    ]


def rows_from(payload):
    """JSON or RSS, whichever came back."""
    try:
        d = json.loads(payload)
        # Solr puts the rows under response.docs
        r = d.get("response") if isinstance(d, dict) else None
        if isinstance(r, dict) and isinstance(r.get("docs"), list):
            return r["docs"]
        for k in ("data", "documents", "records", "results", "items", "docs"):
            v = d.get(k) if isinstance(d, dict) else None
            if isinstance(v, list):
                return v
        if isinstance(d, list):
            return d
    except Exception:
        pass
    items = re.findall(r"<item>(.*?)</item>", payload, re.S | re.I)
    out = []
    for it in items:
        def tag(t):
            m = re.search(r"<%s[^>]*>(.*?)</%s>" % (t, t), it, re.S | re.I)
            return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
        out.append({"title": tag("title"), "link": tag("link"),
                    "description": tag("description"), "pubDate": tag("pubDate")})
    return out


def pick(row, *names):
    for n in names:
        for k, v in row.items():
            if k and n in str(k).lower() and v not in (None, "", []):
                return str(v).strip()
    return ""


def iso2(row):
    t = " ".join(str(v) for v in row.values())
    m = re.search(r"\b([A-Z]{2})\b(?=\s*[-\u2014|:])", t)
    if m and m.group(1) in C:
        return m.group(1)
    for code in C:
        if re.search(r"\b" + code + r"\b", t):
            return code
    return ""


def to_record(row):
    cc = iso2(row)
    if not cc:
        return None
    title = pick(row, "title", "name", "subject") or "Biosafety decision"
    date = ""
    m = re.search(r"(19|20)\d{2}-\d{2}-\d{2}", " ".join(str(v) for v in row.values()))
    if m: date = m.group(0)
    else:
        m = re.search(r"(19|20)\d{2}", " ".join(str(v) for v in row.values()))
        if m: date = m.group(0) + "-01-01"
    link = pick(row, "link", "url", "href") or (BASE + "/database/decisions")
    lat, lng = C[cc]
    return {
        "name": title[:180],
        "source": "bch:decision",
        "type": "National biosafety decision",
        "lat": lat, "lng": lng, "state": cc,
        "precise": False, "impact": 2,
        "company": "", "size": "",
        "status": pick(row, "status", "decision") or "Filed to the Biosafety Clearing-House",
        "phase": "post", "date": date,
        "lapsed": False,
        "url": link,
        "desc": ("WHAT. A national decision on a living modified organism, filed by the "
                 "country itself to the Biosafety Clearing-House. "
                 "WHERE IT SITS. Under Article 20 of the Cartagena Protocol every party "
                 "files its release and market decisions here within fifteen days. 173 "
                 "parties do; **the United States is not one of them.** "
                 "WHY IT MATTERS. This is the only place national release decisions from "
                 "that many countries sit together. A country with no records here has not "
                 "necessarily approved nothing \u2014 it may simply not have filed, and the gap "
                 "between those two is invisible from the outside."),
        "checked": "",
    }


def main():
    print("looking for a machine-readable BCH route")
    rows = []
    for u in endpoints():
        try:
            first = get(u)
        except Exception as e:
            print("  %-58s %s" % (u[:58], str(e)[:34]), file=sys.stderr); continue
        got = rows_from(first)
        if not got:
            continue
        # PAGINATE. The first version asked once for 2,000 rows and stopped,
        # which is why an earlier run reported 460 decisions and I wrongly read
        # that as the total. Solr reports numFound; walk it.
        total = None
        try:
            total = json.loads(first).get("response", {}).get("numFound")
        except Exception:
            pass
        print("  %d rows from %s%s" % (len(got), u[:70],
              (" of %s" % total) if total else ""))
        if total and total > len(got) and "start=" not in u:
            # Page until numFound is reached. There is no record cap: the point
            # of this layer is every decision, and a cap on the count is how the
            # APHIS harvest quietly lost 21,500 records for months.
            #
            # The guard is a wall-clock budget instead, and if it is ever hit the
            # run SAYS SO in the loudest terms available. A truncation nobody is
            # told about is the failure mode worth engineering against.
            budget_s = 900.0
            started, page = time.time(), len(got)
            while page < total:
                if time.time() - started > budget_s:
                    print("    !! STOPPED EARLY at %d of %s after %d minutes. THIS LAYER IS "
                          "INCOMPLETE. Raise budget_s or run with --resume."
                          % (len(got), total, budget_s // 60), file=sys.stderr)
                    break
                sep = "&" if "?" in u else "?"
                try:
                    more = rows_from(get(u + sep + "start=" + str(page)))
                except Exception as e:
                    print("    !! page at %d failed (%s) - LAYER INCOMPLETE"
                          % (page, str(e)[:40]), file=sys.stderr); break
                if not more:
                    break
                got.extend(more); page += len(more)
                if page % 20000 < len(more):
                    print("    %d of %s" % (page, total))
                time.sleep(0.3)
            if len(got) >= total:
                print("    paged to %d of %s - complete" % (len(got), total))
        rows = got
        break

    if not rows:
        print("no BCH route returned records. The portal is a JavaScript application and "
              "its export path has moved before \u2014 open %s/database/decisions, watch the "
              "network tab, and add the URL to endpoints()." % BASE, file=sys.stderr)
        return

    out, noplace = [], 0
    seen = set()
    for r in rows:
        rec = to_record(r)
        if rec is None:
            noplace += 1; continue
        k = rec["name"].lower() + rec["state"]
        if k in seen: continue
        seen.add(k); out.append(rec)

    from collections import Counter
    by = Counter(r["state"] for r in out)
    print("  usable: %d decisions across %d countries" % (len(out), len(by)))
    print("  most-filed: %s" % ", ".join("%s %d" % kv for kv in by.most_common(6)))
    if noplace:
        print("  dropped for no identifiable country: %d" % noplace)

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written"); return
    OUT.write_text(json.dumps({
        "note": ("National biosafety decisions filed to the Biosafety Clearing-House under "
                 "Article 20 of the Cartagena Protocol. Country-level positions. The United "
                 "States is not a party and files nothing here, so this and the APHIS harvest "
                 "are complementary rather than overlapping."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
