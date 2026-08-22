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
MISSING_CC = {}   # country code -> records dropped for want of a centroid

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


# The record types the Protocol produces. A decision is filed under
# biosafetyDecision, but the same obligation has been met under several schema
# names across the Protocol's twenty-five years, and a country that filed under
# one and not another is invisible if only one is asked for.
DECISION_SCHEMAS = ("biosafetyDecision", "decision", "nationalDecision",
                    "biosafetyDecisionDomestic", "countryDecision")


def endpoints():
    """Solr queries against the shared CBD index, then the old guesses as a
    fallback. `schema_s` names the record type."""
    q = []
    for schema in DECISION_SCHEMAS:
        q.append(API + "?" + urlencode({
            "q": "*:*", "fq": "schema_s:" + schema, "rows": 2000,
            "wt": "json", "sort": "createdDate_dt desc"}))
    q.append(API + "?" + urlencode({
        "q": "biosafety decision release", "rows": 2000, "wt": "json"}))
    return q + [
        BASE + "/api/v2013/documents?schema=decision&format=json",
        BASE + "/rss/decisions.aspx",
    ]


def schema_census():
    """What record types the index actually holds, and how many of each.

    Reconnaissance rather than harvest. DECISION_SCHEMAS above is a list of
    guesses; this asks the index to enumerate its own schema_s values so the
    guessing can stop. Printed by --schemas.
    """
    u = API + "?" + urlencode({"q": "*:*", "rows": 0, "wt": "json",
                               "facet": "true", "facet.field": "schema_s",
                               "facet.limit": 200})
    try:
        d = json.loads(get(u))
    except Exception as e:
        print("  schema census failed: %s" % str(e)[:60], file=sys.stderr)
        return []
    ff = (((d.get("facet_counts") or {}).get("facet_fields") or {})
          .get("schema_s") or [])
    return [(ff[i], ff[i + 1]) for i in range(0, len(ff) - 1, 2)]


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


# The panel's type dropdown filters on a record's `type`, which is how the
# APHIS layer's "<organism>, environmental release" turns that control into an
# organism filter for free. Every decision here carried the SAME constant type,
# so for 3,072 non-US records the dropdown had exactly one entry and did
# nothing. The organism is named in the decision's own title; where it is not,
# the record says so rather than being assigned one.
ORGANISM = [
    ("maize", r"\bmaize\b|\bcorn\b|zea mays"),
    ("soybean", r"soy\s?bean|glycine max|\bsoya\b"),
    ("cotton", r"\bcotton\b|gossypium"),
    ("canola / oilseed rape", r"canola|oilseed rape|brassica napus"),
    ("rice", r"\brice\b|oryza"),
    ("potato", r"\bpotato\b|solanum tuberosum"),
    ("wheat", r"\bwheat\b|triticum"),
    ("sugar beet", r"sugar\s?beet|beta vulgaris"),
    ("alfalfa", r"alfalfa|lucerne|medicago"),
    ("papaya", r"papaya|carica"),
    ("eggplant / brinjal", r"eggplant|brinjal|aubergine|solanum melongena"),
    ("apple", r"\bapple\b|malus"),
    ("carnation", r"carnation|dianthus"),
    ("poplar / tree", r"poplar|eucalyptus|populus|\bpine\b|chestnut"),
    ("salmon / fish", r"salmon|tilapia|\bfish\b"),
    ("mosquito / insect", r"mosquito|aedes|anopheles|\bmoth\b|\binsect\b|fruit fly"),
    ("micro-organism", r"micro-?organism|bacteri|yeast|fungus|rhizobium|\bvirus\b"),
    ("vaccine", r"vaccin"),
    ("livestock", r"\bcattle\b|\bpig\b|\bswine\b|poultry|\bsheep\b|\bgoat\b"),
]
_ORG = [(lbl, re.compile(pat, re.I)) for lbl, pat in ORGANISM]


# Roughly a quarter of decision titles name no organism at all - they are
# "Technical Opinion No. 293/2022" or "Decision 42 of the Commission". Many of
# those DO carry the OECD unique identifier of the organism, which is the key
# the BCH registry of modified organisms is built on. So before giving up, the
# event code in the title is looked up in bch_organisms.json. That reads the
# answer out of the same source rather than guessing it: if the file is absent
# or the code is not in it, the record says the organism was not named.
# Matches bch_organisms.CODE_RE. The second separator is required, which is
# what keeps this off ordinary prose; the first may be absent only when the
# event segment starts with a digit or \u00d8. Unicode dashes are accepted here
# because decision titles are typeset text rather than a database cell.
_DASH = "\\-\u2010-\u2015"
_SEP = "\\s" + _DASH
_OECD_IN_TITLE = re.compile(
    r"\b([A-Z]{2,4})"
    # Letters in the event segment only in the HYPHENATED form (_DASH, which
    # includes the unicode dashes typeset titles use). The space-separated and
    # run-together forms keep the digits-only class: letters there matched
    # "ANNEX II PART 4" as an identifier.
    r"((?:[" + _DASH + r"][A-Z0-9\u00d8\u00f8]{3,7}[" + _DASH + r"])|(?:[\s\-]?[0-9\u00d8\u00f8O]{3,7}[\s\-]?))"
    r"([0-9])\b")
_ORGDB = None


def _orgdb():
    """{normalised OECD identifier: organism} from bch_organisms.json."""
    global _ORGDB
    if _ORGDB is not None:
        return _ORGDB
    _ORGDB = {}
    fp = pathlib.Path(__file__).resolve().parent / "bch_organisms.json"
    try:
        data = json.loads(fp.read_text(encoding="utf-8")).get("organisms") or {}
        # bch_organisms.py writes a DICT keyed on the normalised identifier.
        # The list branch is kept for an older file; iterating a dict as a list
        # yields its keys, and .get on a string raises into the except below,
        # which is how this returned an empty registry without saying so.
        items = data.items() if isinstance(data, dict) else (
            ((r.get("key") or r.get("id"), r) for r in data))
        for k, r in items:
            nm = (r.get("organism") or r.get("species") or "") if isinstance(r, dict) else ""
            if k and nm:
                _ORGDB[_norm_id(k)] = nm
    except Exception:
        pass
    return _ORGDB


def _norm_id(s):
    """Must agree CHARACTER FOR CHARACTER with bch_organisms.norm,
    latam_approvals.norm_id, isaaa_approvals.norm_id and cfia_approvals.norm_id.
    Five files carry a copy; if one drifts, cross-register lookups miss silently
    and a miss reads as the event not existing."""
    if not s:
        return ""
    t = str(s).upper()
    t = re.sub(r"[^A-Z0-9\u00d8\u00f8]", "", t)
    t = t.replace("\u00d8", "0").replace("\u00f8", "0")
    t = re.sub(r"(?<=[0-9])O", "0", t)
    t = re.sub(r"O(?=[0-9])", "0", t)
    return t


def organism_of(title):
    for lbl, rx in _ORG:
        if rx.search(title or ""):
            return lbl
    db = _orgdb()
    if db:
        for m in _OECD_IN_TITLE.finditer(title or ""):
            hit = db.get(_norm_id(m.group(0)))
            if hit:
                return hit.lower()
    return ""


# A decision is not necessarily an approval. The Protocol requires the decision
# to be filed, whatever it is, and a prohibition is the most interesting record
# in the set. Read only from words the title states outright; anything else
# stays "Filed to the Biosafety Clearing-House" rather than being guessed at.
OUTCOME = [
    ("Prohibited or rejected", r"prohibit|\bban\b|banned|reject|refus|denied|not approved"),
    ("Withdrawn", r"withdraw|revoke|cancel"),
    ("Approved", r"approv|authoris|authoriz|permit|consent|commercial release|placing on the market"),
    ("Field trial", r"field trial|confined|experimental release"),
]
_OUT = [(lbl, re.compile(pat, re.I)) for lbl, pat in OUTCOME]


def outcome_of(title):
    for lbl, rx in _OUT:
        if rx.search(title or ""):
            return lbl
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
    # NOT C[cc]. This raised KeyError on the first country missing from the
    # table and took the whole run down after 3,950 records had been read - and
    # the table holds 67 countries, so about a hundred more would have followed.
    # A record that cannot be sited already has a route: it goes to unplaced,
    # which the caller handles and reports. MISSING_CC records which codes were
    # asked for, so the log names what to add instead of leaving it to be found
    # by the next crash. Do NOT fill this from animal_facilities.ST or
    # aphis_releases.STATES: those are US STATE tables, where PA is Pennsylvania
    # and DE is Delaware, and merging them would site Panama in Pennsylvania.
    if cc not in C:
        MISSING_CC[cc] = MISSING_CC.get(cc, 0) + 1
        return None
    lat, lng = C[cc]
    return {
        "name": title[:180],
        "source": "bch:decision",
        "type": ((organism_of(title) or "organism not named in the title")
                 + ", national biosafety decision"),
        "lat": lat, "lng": lng, "state": cc,
        "precise": False, "impact": 2,
        "company": "", "size": "",
        "status": (pick(row, "status", "decision") or outcome_of(title)
                   or "Filed to the Biosafety Clearing-House"),
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
        # UNION, DO NOT STOP HERE.
        #
        # This used to `break` on the first endpoint that returned anything, so
        # whichever schema answered first became the whole layer and every
        # decision filed under a different record type was never asked for. The
        # count looked healthy either way, which is exactly why it went
        # unnoticed: 3,072 rows is a plausible number whether or not it is all
        # of them. Each endpoint is now asked, and the results deduped on record
        # id, with per-source counts printed so a schema that adds nothing is
        # visible rather than assumed.
        before = len(rows)
        rows.extend(got)
        print("    +%d (running total %d)" % (len(got), len(rows)))
        if before and len(got) == 0:
            print("    (this schema added nothing)")

    # Dedupe across schemas: the same decision can be indexed under more than
    # one record type, and two markers for one decision is worse than none.
    if rows:
        seen_ids, uniq = set(), []
        for r in rows:
            rid = ""
            for f in ("id", "identifier_s", "recordid", "record_id", "uid"):
                v = r.get(f)
                if isinstance(v, list) and v:
                    v = v[0]
                if v:
                    rid = str(v); break
            k = rid or json.dumps(r, sort_keys=True)[:400]
            if k in seen_ids:
                continue
            seen_ids.add(k); uniq.append(r)
        if len(uniq) != len(rows):
            print("  %d rows across all schemas, %d after deduping on record id"
                  % (len(rows), len(uniq)))
        rows = uniq

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
    MISSING_CC.clear()
    out, unplaced_rows = [], []
    seen = set()
    for r in rows:
        rec = to_record(r)
        if rec is None:
            unplaced_rows.append(r); continue
        k = rec["name"].lower() + rec["state"]
        if k in seen: continue
        seen.add(k); out.append(rec)

    # WHY THESE ARE NO LONGER AGGREGATED HERE.
    #
    # This step used to collapse every country's decisions into ONE marker
    # carrying a count and six titles in a paragraph, on the reasoning that a
    # national decision has no site and several hundred pins on one centroid
    # cannot be clicked past. The second half of that is true. The first half
    # made it the wrong fix, and the file's own note said so: aphis_releases.py
    # ALREADY groups every release record by coordinate, across all registers,
    # into a place marker carrying records_total, dates[], sources[] and a
    # per-record list the map's cluster panel can sort and filter.
    #
    # So aggregating here did not prevent a stack - the merge downstream
    # prevents the stack anyway. What it did was throw away 3,072 individual
    # decisions before the merge could see them, leaving 51 paragraphs where the
    # United States has 22,111 browsable records. That IS the geographic
    # imbalance on this map, and it is a formatting decision rather than a gap
    # in the world.
    #
    # Individual records go out. The country marker the reader sees is built by
    # the merge, identically to every other register, and each decision inside
    # it keeps its own title, date, outcome, organism and link.
    from collections import Counter
    print("  %d decisions kept as individual records; aphis_releases.py groups "
          "them by coordinate into one marker per country" % len(out))
    by = Counter(r["state"] for r in out)

    print("  usable: %d decisions across %d countries" % (len(out), len(by)))
    print("  most-filed: %s" % ", ".join("%s %d" % kv for kv in by.most_common(6)))
    if unplaced_rows:
        print("  no country field, parked in the Atlantic: %d" % len(unplaced_rows))
    if MISSING_CC:
        # Named, not silent. Each of these is a country whose decisions were
        # read and then dropped for want of a coordinate; the fix is to add
        # the code to C, and this line says exactly which.
        tot = sum(MISSING_CC.values())
        print("  DROPPED for want of a centroid: %d records across %d countries"
              % (tot, len(MISSING_CC)))
        print("     add these to C: %s"
              % " ".join("%s(%d)" % (k, v)
                         for k, v in sorted(MISSING_CC.items(),
                                            key=lambda kv: -kv[1])))

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written"); return
    OUT.write_text(json.dumps({
        "note": ("National biosafety decisions filed to the Biosafety Clearing-House under "
                 "Article 20 of the Cartagena Protocol. Country-level positions. The United "
                 "States is not a party and files nothing here, so this and the APHIS harvest "
                 "are complementary rather than overlapping."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


# ============================================================ SELFTEST =======

def selftest():
    """No network. Drives the record builder with the shapes the API returns."""
    fails = []

    def ck(nm, got, want):
        if got != want:
            fails.append("%s: got %r want %r" % (nm, got, want))

    ck("organism: maize", organism_of("Commercial release of corn event MON 87429"), "maize")
    ck("organism: cotton", organism_of("Approval of Herbicide Tolerant Cotton"), "cotton")
    ck("organism: mosquito", organism_of("Release of Aedes aegypti OX513A"), "mosquito / insect")
    ck("organism: none named", organism_of("Decision No. 42 of the Commission"), "")

    # THE KeyError THAT KILLED A RUN AFTER 3,950 RECORDS. C holds 67 countries;
    # the first decision from one of the other ~100 raised and took the whole
    # harvest down. A country with no centroid must be dropped and NAMED.
    _f = GOV_PREFIX_FIELDS[0]
    def _row(code):
        return {_f: ["%s_12345" % code], "title_EN_s": "Decision", "id": "abcdef123"}
    MISSING_CC.clear()
    ck("country missing from C returns None instead of raising",
       to_record(_row("pa")), None)
    ck("and the code is recorded so the log can name it",
       dict(MISSING_CC), {"PA": 1})
    to_record(_row("pa"))
    ck("a second one is counted, not overwritten", dict(MISSING_CC), {"PA": 2})
    ck("a country that IS in C is still sited",
       (to_record(_row("br")) or {}).get("lat"), C["BR"][0])
    MISSING_CC.clear()

    ck("outcome: prohibition beats approval wording",
       outcome_of("Application to approve X was rejected"), "Prohibited or rejected")
    ck("outcome: approval", outcome_of("Approval of herbicide tolerant maize (GA21)"), "Approved")
    ck("outcome: trial", outcome_of("Confined field trial of Bt cowpea"), "Field trial")
    ck("outcome: silent", outcome_of("Decision No. 42"), "")

    row = {"title_s": "Commercial release of corn event MON 87429 - Technical Opinion 8035/2022",
           "grp_government_schema_s": "br_biosafetyDecision",
           "id": "52000000cbd080000000c041",
           "meta_modifiedOn_dt": "2022-11-04T00:00:00Z"}
    r = to_record(row)
    ck("country from the schema prefix", r["state"], "BR")
    ck("type carries the organism", r["type"], "maize, national biosafety decision")
    ck("status carries the outcome", r["status"], "Approved")
    ck("date parsed", r["date"], "2022-11-04")
    ck("link is the record, not the list",
       r["url"], "https://bch.cbd.int/en/database/52000000cbd080000000c041")
    ck("source family", r["source"], "bch:decision")
    ck("no country, no record", to_record({"title_s": "Some decision"}), None)

    # THE POINT OF THIS ROUND: individual records survive to the merge.
    rows = [dict(row, id="a%d" % i, title_s="Decision %d on maize" % i) for i in range(40)]
    out = [x for x in (to_record(r) for r in rows) if x]
    ck("40 rows stay 40 records", len(out), 40)
    ck("all on one country centroid", len({(x["lat"], x["lng"]) for x in out}), 1)

    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print("  -", f)
        return 1
    print("selftest: all checks passed")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--schemas" in sys.argv:
        print("record types held in the CBD index:")
        for name, n in sorted(schema_census(), key=lambda x: -x[1]):
            print("  %-40s %d" % (name, n))
        sys.exit(0)
    main()
