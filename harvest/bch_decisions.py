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


# The field discovery run settled this. The index stores the country in three
# usable shapes and the one this list was reading first, government_s, holds a
# two-letter code rather than a name - which is why 2,867 of 2,918 decisions
# were dropped as having no country. The English name is government_EN_s, with
# a capital EN; the lowercase spelling that used to be tried does not exist.
#
# The code field is kept, last, because a code is still a country: it is mapped
# through ISO2 rather than discarded.
# THE COUNTRY IS A PREFIX, NOT A FIELD.
#
# Two rounds were spent on this. The discovery run showed government_EN_s on a
# CONTACT record and that field was added here - and the count stayed at 51,
# because a DECISION record does not carry it. What a decision record carries
# is:
#
#     grp_government_schema_s        za_biosafetyDecision
#
# The country is the ISO2 code glued to the front of the schema name. No field
# on the record holds it on its own, which is why every field-name guess failed
# and why 2,854 of 2,905 decisions were dropped as having no country.
GOV_PREFIX_FIELDS = ("grp_government_schema_s", "grp_government_s",
                     "government_schema_s")


def government_from_prefix(doc):
    """Pull the ISO2 code off the front of the grouping field."""
    for f in GOV_PREFIX_FIELDS:
        v = doc.get(f)
        if isinstance(v, list):
            v = v[0] if v else None
        if not v:
            continue
        s = str(v)
        if "_" in s:
            code = s.split("_", 1)[0].strip().lower()
            if len(code) == 2 and code.isalpha():
                return code.upper()
    return None


COUNTRY_FIELDS = ("government_EN_s", "country_EN_s", "government_EN_t",
                  "country_EN_t", "countryRegions_EN_ss",
                  "government_s", "country_s", "government_REL_ss",
                  "countries_ss", "owner_s", "jurisdiction_s")


# The organism registry, used to resolve a decision title that carries only an
# event code. About a quarter of BCH titles name no organism - they read
# "Technical Opinion No. 293/2022" - and many of those carry the code.
_ORG_REG = None


def _org_registry():
    global _ORG_REG
    if _ORG_REG is None:
        _ORG_REG = {}
        try:
            f = pathlib.Path(__file__).resolve().parent / "bch_organisms.json"
            if f.exists():
                _ORG_REG = json.loads(f.read_text(encoding="utf-8")).get(
                    "organisms", {})
        except Exception:
            _ORG_REG = {}
    return _ORG_REG


def _norm_id(code):
    """Must match bch_organisms.norm exactly, or every lookup misses and the
    miss looks like the organism not being registered."""
    if not code:
        return ""
    s = str(code).upper()
    s = re.sub(r"[^A-Z0-9\u00d8\u00f8]", "", s)
    s = s.replace("\u00d8", "0").replace("\u00f8", "0")
    s = re.sub(r"(?<=[0-9])O", "0", s)
    s = re.sub(r"O(?=[0-9])", "0", s)
    return s


_CODE_RE = re.compile(r"\b([A-Z]{2,4})[\s\-]?([0-9\u00d8O]{3,7})[\s\-]?([0-9])\b")


def organism_from_registry(title):
    """The organism behind an event code in a title, or nothing.

    Nothing is the honest answer when the code is unknown: the record then says
    the organism was not named, rather than carrying a guess.
    """
    m = _CODE_RE.search(str(title or "").upper())
    if not m:
        return None
    rec = _org_registry().get(_norm_id("-".join(m.groups())))
    if not rec:
        return None
    return rec.get("organism") or rec.get("name") or None


def iso2(row):
    """The country that filed the decision, read from the field that states it.

    The first version scanned the whole record for any two-letter code. Spanish
    and French decision text is full of two-letter fragments, so records like
    "Documento de Decision de la solicitud de liberacion al ambiente" were being
    filed under Germany. **Never infer a country from free text when the record
    has a field for it** - and if the field is missing, drop the record rather
    than guess, because a decision placed in the wrong country is worse than a
    decision that is absent.
    """
    # The prefix first: it is on nearly every record, and the named fields are
    # on almost none.
    _p = government_from_prefix(row)
    if _p:
        return _p
    for f in COUNTRY_FIELDS:
        for k, v in row.items():
            if str(k).lower() != f:
                continue
            for cand in (v if isinstance(v, list) else [v]):
                c = str(cand).strip().upper()[:2]
                if c in C:
                    return c
    # last resort: an explicit code at the very start, e.g. "BR - Decision on..."
    title = str(row.get("title_s") or row.get("title") or "")
    m = re.match(r"\s*([A-Z]{2})\s*[-\u2014|:]", title)
    return m.group(1) if m and m.group(1) in C else ""


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
    # BCH record pages are /en/database/{recordId}. The generic list URL was
    # being emitted for every record, so no link went anywhere useful.
    rid = ""
    for f in ("id", "identifier_s", "recordid", "record_id", "uid"):
        v = pick(row, f)
        if v and len(v) > 4:
            rid = v.split("/")[-1]; break
    link = (BASE + "/en/database/" + rid) if rid else pick(row, "url", "link", "href")
    if not link or not link.startswith("http"):
        link = BASE + "/en/database/?currentid=" + rid if rid else BASE + "/database/decisions"
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
        "desc": ("A decision on a living modified organism, filed by the country itself "
                 "to the Biosafety Clearing-House. Article 20 of the Cartagena Protocol "
                 "requires every party to file its release and market decisions there "
                 "within fifteen days, and 173 parties are bound by it. The United States "
                 "is not among them. Nowhere else holds national release decisions from "
                 "this many countries in one place. A country with no records here has not "
                 "necessarily approved nothing \u2014 it may not have filed, and from the "
                 "outside those two look the same."),
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

    # A record whose country field is missing is still a real decision. Dropping
    # it hides a gap in the source; putting it in a plausible country would be a
    # lie. So it goes to a marked spot in the mid-Atlantic, where no reader can
    # mistake it for a place, and the entry says why it is there.
    UNPLACED = (14.5, -38.0)
    out, unplaced_rows = [], []
    seen = set()
    for r in rows:
        rec = to_record(r)
        if rec is None:
            unplaced_rows.append(r); continue
        k = rec["name"].lower() + rec["state"]
        if k in seen: continue
        seen.add(k); out.append(rec)

    # A national decision has no site - it applies to a whole country - so every
    # record in a country lands on the same centroid. Several hundred markers
    # stacked on one point is not a map; you cannot click past the top one.
    #
    # So they are aggregated: ONE marker per country carrying the count, the
    # date range, and the most recent decisions by name. The detail is in the
    # entry rather than in hundreds of dots that cannot be separated, because
    # spreading them into a ring would invent geography the source does not have.
    from collections import Counter, defaultdict
    grouped = defaultdict(list)
    for r in out:
        grouped[r["state"]].append(r)

    agg = []
    for cc, rs in grouped.items():
        rs.sort(key=lambda x: x.get("date", ""), reverse=True)
        dates = [x["date"][:4] for x in rs if x.get("date")]
        span = ("%s\u2013%s" % (min(dates), max(dates))) if dates else ""
        recent = "; ".join(x["name"][:90] for x in rs[:6])
        agg.append({
            "name": "%s \u2014 %d biosafety decision%s filed" % (cc, len(rs), "" if len(rs) == 1 else "s"),
            "source": "bch:decision",
            "type": "National biosafety decisions",
            "lat": rs[0]["lat"], "lng": rs[0]["lng"], "state": cc,
            "precise": False, "impact": 3 if len(rs) > 20 else 2,
            "company": "", "size": "%d decisions" % len(rs),
            "status": ("Filed %s" % span) if span else "Filed to the Biosafety Clearing-House",
            "phase": "post", "date": rs[0].get("date", ""), "lapsed": False,
            "url": rs[0]["url"],
            # The three labelled sections said the same thing about every country
            # with two numbers changed. Written as prose the country's own
            # figures carry the paragraph instead.
            "desc": ("%d decision%s on living modified organisms, filed by this country "
                     "to the Biosafety Clearing-House%s. The most recent are %s. "
                     "Article 20 of the Cartagena Protocol requires every party to file "
                     "its release and market decisions there within fifteen days, and 173 "
                     "parties are bound by it; the United States is not among them. "
                     "A decision is a national instrument with no site to place, so this "
                     "marker sits at the country centroid and holds all of them together "
                     "rather than scattering them into a geography the source does not "
                     "have. A country with no records here has not necessarily approved "
                     "nothing \u2014 it may not have filed."
                     % (len(rs), "" if len(rs) == 1 else "s",
                        (", %s" % span) if span else "", recent or "not stated")),
            "checked": "",
        })
    # NOTE: these country markers are merged again by aphis_releases.py, which
    # groups every release record by coordinate regardless of which register it
    # came from. That is the merge the map actually shows. This grouping only
    # stops a country's decisions arriving as hundreds of identical points.
    print("  grouped %d decisions into %d country markers" % (len(out), len(agg)))
    out = agg

    by = Counter(r["state"] for r in out)
    if unplaced_rows:
        agg.append({
            "name": "%d decisions with no country stated" % len(unplaced_rows),
            "source": "bch:decision", "type": "Filed without a country field",
            "lat": UNPLACED[0], "lng": UNPLACED[1], "state": "\u2014",
            "precise": False, "impact": 2, "company": "",
            "size": "%d decisions" % len(unplaced_rows),
            "status": "Country not stated in the record", "phase": "post",
            "date": "", "lapsed": False, "url": BASE + "/database/decisions",
            "desc": ("WHAT. %d decisions filed to the Biosafety Clearing-House whose record "
                     "carries no country field. "
                     "WHERE IT SITS. **Nowhere. This marker is in the middle of the Atlantic "
                     "because there is no ocean release and no country to place these in** \u2014 it "
                     "is a visible parking space, not a location. "
                     "WHY IT MATTERS. Dropping them would hide a gap in the source; putting them "
                     "in a plausible country would be a fabrication. They are counted here so the "
                     "total stays honest and the missing field stays visible."
                     % len(unplaced_rows)),
            "checked": "",
        })
        out = agg
        by = Counter(r["state"] for r in out)
    print("  usable: %d decisions across %d countries" % (len(out), len(by)))
    print("  most-filed: %s" % ", ".join("%s %d" % kv for kv in by.most_common(6)))
    if unplaced_rows:
        print("  no country field, parked in the Atlantic: %d" % len(unplaced_rows))

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
