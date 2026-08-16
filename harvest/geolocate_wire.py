#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pin wire items onto the map, at local level only.

Built to GEOLOCATING_A_NEWS_FEED.md. The one rule everything else serves:

    NEVER INVENT A LOCATION.

An item either resolves to a place this map already holds coordinates for, or
it gets no pin. There is no geocoding of place names out of article text,
because that is how "Cambridge" lands on the wrong continent.

WHY THE CORPUS IS SMALL ON PURPOSE.

Only places we hold at street or mapped precision are eligible - clinics with a
geocoded address, OSM points somebody stood at, facilities placed at their own
door. Everything at 'administrative' or 'centroid' grade is excluded, which
removes every corporate head office and every country centroid from the corpus
at a stroke. That is deliberate twice over: it is what makes a pin local rather
than national, and it sidesteps the failure the brief is most emphatic about -
a company name identifies a company, never one of its fifty sites.

WHAT SUCCESS LOOKS LIKE.

Well under one per cent of items mapped. The brief's own build managed 23 of
9,000. A busy version of this feature is the version nobody can trust, and every
guard below exists because something wrong got through somewhere.

    python3 harvest/geolocate_wire.py
    python3 harvest/geolocate_wire.py --selftest      # no network needed
    python3 harvest/geolocate_wire.py --max-age-days 365
"""

import json, gzip, re, sys, time, math, pathlib, unicodedata
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
WIRE = ROOT / "wire.json"
PROJECTS = ROOT / "projects.json.gz"
OUT = ROOT / "wire_geo.json"
REPORT = HERE / "wire_geo_report.json"

MIN_OVERLAP = 2          # distinctive tokens shared
MAX_NAME_TOKENS = 8
RARE_MAX_DF = 40         # a token in more than this many entities cannot pin

# ---------------------------------------------------------------------------
# Guards. Each is here because of a specific wrong pin, in this domain or the
# one the brief was written from.
# ---------------------------------------------------------------------------

# Industrial vocabulary is also ordinary English, and this domain's is worse
# than most. Multilingual, because the feed is: 470 of 650 items are not
# English, and an English-only guard silently only guards the English subset.
METAPHOR = re.compile(
    r"(seeds? of (doubt|change|hope|discord)|gene pool of|genetically predisposed|"
    r"cross[- ]pollinat\w* of ideas|hybrid work|frankenstein|"
    r"in the (dna|genes) of|cultural dna|harvest\w* (data|user|attention)|"
    r"crop of (new|young|fresh)|planting the seeds?|"
    r"grain of (truth|salt)|bitter harvest|"
    r"graines? de (doute|discorde)|semillas? de (duda|esperanza)|"
    r"saat des|frucht der arbeit)", re.I)

# Real news about the entities, but not located news.
MARKET = re.compile(
    r"(shares?|stock|shareholder|earnings|quarterly results|guidance|"
    r"market cap|analyst|upgrade[sd]? to|price target|dividend|ipo\b|"
    r"acqui(re|sition)|merger|takeover|profit|revenue|"
    r"acciones|bolsa|beneficios|b\u00f6rse|aktie|gewinn|"
    r"march\u00e9 boursier|b\u00e9n\u00e9fice)", re.I)

# If the only geography an item offers is national or larger, it must not
# become a point. "Brazil approves GM wheat" is real news; pinning it to one
# trial site in Parana invents specificity the story does not have.
SUPRALOCAL = re.compile(
    r"(nationwide|nationally|national (policy|ban|target|plan|rules?|law)|"
    r"federal (government|policy|court|agency|rules?)|countrywide|"
    r"across the country|statewide|eu[- ]wide|european union|"
    r"global(ly)?|worldwide|international (treaty|agreement)|"
    r"world health|united nations|"
    r"landesweit|bundesweit|bundesregierung|europaweit|"
    r"a nivel nacional|en todo el pa\u00eds|gobierno federal|"
    r"\u00e0 l'\u00e9chelle nationale|gouvernement f\u00e9d\u00e9ral|"
    r"em todo o pa\u00eds|governo federal)", re.I)

# For an item to be ABOUT a place it usually names a kind of place.
SITE_WORDS = re.compile(
    r"(field trial|trial site|test plot|greenhouse|glasshouse|nursery|"
    r"seed farm|research station|breeding cent(re|er)|processing plant|"
    r"elevator|silo|laboratory|lab\b|clinic|hospital|facility|farm|plot|"
    r"campus|vivarium|plantation|orchard|"
    r"ensayo de campo|parcela|invernadero|granja|planta|laboratorio|cl\u00ednica|"
    r"essai en champ|serre|ferme|usine|laboratoire|clinique|"
    r"freisetzung|versuchsfeld|gew\u00e4chshaus|labor\b|klinik|"
    r"campo experimental|fazenda|estufa)", re.I)

COMMON = set("""more most best will would people first year years time help open close
back down new news says said after before under over about into other than that this
these those from with have has had been being they their there where when what which
which who whom whose can could may might must shall should also just only very much
many some any each every both few less least still already again against between
during without within across around through report reports study studies plan plans
work works make made take taken give given call called come came know known think
thought long short high low big small good great last next early late public private
local national state federal world global group company companies market markets""".split())

# Domain filler: words that are in half the corpus and pin nothing.
STOP = set("""trial trials field fields test tests plot plots variety varieties line
lines event events crop crops seed seeds sample samples study program programme
project site area centre center institute institut research laboratory lab clinic
clinics hospital university college department division unit units group holdings
limited ltd inc incorporated corporation corp company co gmbh sa sas bv nv plc
pty llc international national regional global services solutions technologies
technology sciences science health medical care fertility reproductive animal
animals plant plants agricultural agriculture biotech biotechnology genetics
genetic""".split())


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def toks(s):
    s = strip_accents(str(s or "").lower())
    return [t for t in re.split(r"[^a-z0-9]+", s) if t]


def seq_of(ts):
    """The name as a phrase, with only ordinary English removed.

    STOP must NOT be applied here. It holds clinic, centre, fertility,
    laboratory - which is to say, the words real entity names are made of.
    Stripping them left "Aberdeen Fertility Centre" as the single token
    "aberdeen", short of the two-token minimum, so the entity was dropped from
    the corpus before any article could match it. Every clinic in the register
    was disappearing the same way, and the run reported a confident zero.
    """
    return [t for t in ts if len(t) > 2 and t not in COMMON]


def distinctive(ts):
    """The rare part of a name, used to decide whether a match means anything.

    Here STOP belongs: a match resting only on "fertility" and "clinic" is not
    a match. It governs scoring, not membership.
    """
    return [t for t in ts if len(t) > 2 and t not in COMMON and t not in STOP]


def contiguous(needle, hay_tokens):
    """The single highest-value guard. Bag-of-words alone matches
    'Green Valley Mine' to an article with green, valley and mine in three
    unrelated sentences."""
    n = len(needle)
    if not n:
        return False
    for i in range(len(hay_tokens) - n + 1):
        if hay_tokens[i:i + n] == needle:
            return True
    return False


# ---------------------------------------------------------------------------
def load_corpus():
    """Places held at street or mapped precision, and nothing else."""
    if not PROJECTS.exists():
        return []
    op = gzip.open if PROJECTS.suffix == ".gz" else open
    try:
        d = json.load(op(PROJECTS, "rt", encoding="utf-8"))
    except Exception as e:
        print("  projects unreadable (%s)" % e, file=sys.stderr)
        return []
    out = []
    for p in (d.get("projects") or []):
        if p.get("lat") is None or p.get("lng") is None:
            continue
        grade = p.get("addr_grade") or ("operational" if p.get("precise") else "")
        if grade not in ("operational", "mapped"):
            continue
        nm = str(p.get("name") or "").strip()
        t = seq_of(toks(nm))
        # One-word names match everything; very long ones match by chance.
        if len(t) < 2 or len(t) > MAX_NAME_TOKENS:
            continue
        if not distinctive(t):
            continue          # nothing rare in it at all
        out.append({"name": nm, "toks": t,
                    "lat": float(p["lat"]), "lng": float(p["lng"]),
                    "iso": iso_of(p), "type": p.get("type") or "",
                    "url": p.get("url") or ""})
    return out


ISO2 = re.compile(r"^[A-Z]{2}$")


def iso_of(p):
    """Best country code the record offers, or blank."""
    st = str(p.get("state") or "")
    m = re.search(r"\b([A-Z]{3})\b", st)
    return m.group(1) if m else ""


def df_ceiling(corpus):
    df = Counter()
    for e in corpus:
        for t in set(e["toks"]):
            df[t] += 1
    return df


def match(item, corpus, df, reasons):
    text = " ".join(str(item.get(k) or "") for k in ("title", "snippet"))
    if not text.strip():
        reasons["empty"] += 1
        return None
    if METAPHOR.search(text):
        reasons["metaphor"] += 1
        return None
    if MARKET.search(text):
        reasons["sector_or_market"] += 1
        return None
    if SUPRALOCAL.search(text):
        # Refused rather than pinned. A country-level layer for these would be
        # a different feature and must not share the point layer.
        reasons["supralocal"] += 1
        return None
    # The site-word test runs AFTER a name match, not before it. Run first it
    # refused 571 of 650 items on the real feed - including any story that
    # names a clinic by its name without using the word "clinic" - and the
    # cheapest guard was doing the most damage. A story that names one of our
    # places by name is about a place whether or not it also says "facility".
    site_ok = bool(SITE_WORDS.search(text))

    hay = seq_of(toks(text))
    if not hay:
        reasons["no_tokens"] += 1
        return None

    best = None
    for e in corpus:
        # The whole name, in order, in the text. This is the guard that does
        # the work; everything else only decides whether the hit is worth
        # anything.
        if not contiguous(e["toks"], hay):
            continue
        shared = [t for t in e["toks"] if t in hay]
        if len(shared) < MIN_OVERLAP:
            continue
        # At least one rare word of our own. A phrase made entirely of
        # "fertility clinic" is a description, not a name.
        rare = [t for t in distinctive(e["toks"])
                if t in hay and df.get(t, 0) <= RARE_MAX_DF]
        if not rare:
            continue
        score = len(shared) + sum(1.0 / max(1, df.get(t, 1)) for t in rare)
        if best is None or score > best[0]:
            best = (score, e)
    if best is None:
        reasons["no_place_match"] += 1
        return None

    e = best[1]
    # Now the site word earns its place: it breaks a tie the name alone cannot,
    # and a single-token-overlap match without one is not worth the risk.
    if not site_ok and len([t for t in e["toks"] if t in hay]) < 3:
        reasons["names_no_place_kind"] += 1
        return None
    # Region gate: a story that names a country other than the entity's is not
    # about the entity. This caught a Spanish site matching a Mexican one.
    iso = str(item.get("iso") or "").upper()
    if iso and e["iso"] and iso != e["iso"]:
        reasons["country_mismatch"] += 1
        return None
    # Coordinate sanity, which catches corruption rather than mismatching.
    if not (abs(e["lat"]) <= 90 and abs(e["lng"]) <= 180):
        reasons["bad_coordinates"] += 1
        return None

    return {"link": item.get("link"), "title": item.get("title"),
            "date": item.get("date"), "lang": item.get("lang"),
            "source": item.get("name"),
            "place": e["name"], "type": e["type"],
            "lat": e["lat"], "lng": e["lng"], "iso": e["iso"],
            "score": round(best[0], 3)}


# ---------------------------------------------------------------------------
def selftest():
    """Fixtures drawn from real failures. Every wrong pin becomes permanent."""
    fails = []
    # Built the way load_corpus builds it, or the fixture tests something the
    # real code never does. Written by hand once, "fertility" survived here and
    # was stripped there, and the test reported a lost match that was only the
    # fixture disagreeing with the loader.
    corpus = [{"name": "Green Valley Fertility Clinic",
               "toks": seq_of(toks("Green Valley Fertility Clinic")),
               "lat": 51.5, "lng": -0.1, "iso": "GBR", "type": "", "url": ""}]
    df = df_ceiling(corpus)

    def m(title, **kw):
        it = {"title": title, "snippet": "", "link": "x", "date": "", "lang": "en"}
        it.update(kw)
        return match(it, corpus, df, Counter())

    # things that must NEVER pin
    for bad in ("A gold mine of tax breaks for the clinic",
                "Seeds of doubt at the research station",
                "Shares rose 4% as the plant reopened",
                "Nationwide ban on the field trial programme",
                "Green things happen in the valley, and fertility is up",
                # word order matters: the same words, rearranged, is a
                # different place or no place
                "Fertility clinic in the green valley expands",
                "Valley Green Fertility Clinic opens"):
        if m(bad):
            fails.append("regression: " + bad)
    # real ones must survive. A guard tightened past usefulness looks exactly
    # like a guard working, and only this list tells the difference.
    for good in ("Green Valley Fertility Clinic wins planning appeal",
                 "Inspectors visit Green Valley Fertility Clinic this week"):
        if not m(good):
            fails.append("lost-a-real-match: " + good)
    # country gate
    if m("Green Valley Fertility Clinic expands", iso="MEX"):
        fails.append("country gate did not fire")
    # an entity whose name holds nothing rare must never enter the corpus
    if load_corpus.__doc__ and distinctive(seq_of(toks("Fertility Clinic"))):
        fails.append("a name made only of domain words was treated as rare")

    n = 11
    print("selftest: %d checks, %d failures" % (n, len(fails)))
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    max_age = 365
    if "--max-age-days" in sys.argv:
        max_age = int(sys.argv[sys.argv.index("--max-age-days") + 1] or 365)

    if not WIRE.exists():
        print("no wire.json; nothing to do", file=sys.stderr)
        return
    items = json.loads(WIRE.read_text(encoding="utf-8"))
    corpus = load_corpus()
    df = df_ceiling(corpus)
    print("  %d wire items against %d places held at street or mapped precision"
          % (len(items), len(corpus)))
    if not corpus:
        print("  the corpus is empty - every place this map holds is at "
              "administrative or centroid grade, so nothing can be pinned "
              "locally. Run the facility harvesters first.", file=sys.stderr)
        return

    reasons = Counter()
    fresh = [r for r in (match(i, corpus, df, reasons) for i in items) if r]

    # Accumulate rather than replace. The feed keeps a rolling window, so
    # regenerating from scratch quietly discards every pin older than it and
    # makes a working geolocator look like a broken one.
    prior = []
    if OUT.exists():
        try:
            prior = json.loads(OUT.read_text(encoding="utf-8")).get("pins", [])
        except Exception:
            prior = []
    cutoff = time.time() - max_age * 86400
    def keep(r):
        try:
            return time.mktime(time.strptime(str(r.get("date"))[:10], "%Y-%m-%d")) >= cutoff
        except Exception:
            return True
    merged, seen = [], set()
    for r in fresh + [p for p in prior if keep(p)]:
        k = (r.get("link"), r.get("place"))
        if k in seen:
            continue
        seen.add(k)
        merged.append(r)

    print("  mapped %d of %d this run (%d after merge)"
          % (len(fresh), len(items), len(merged)))
    for k, v in reasons.most_common():
        print("     refused, %-22s %d" % (k, v))

    OUT.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d"),
                               "note": ("Wire items resolved to places this map "
                                        "already holds at street precision. An "
                                        "item that resolves to nothing gets no "
                                        "pin."),
                               "pins": sorted(merged, key=lambda r: str(r.get("date")),
                                              reverse=True)},
                              ensure_ascii=False, indent=1, sort_keys=True),
                   encoding="utf-8")
    REPORT.write_text(json.dumps({"wire_items": len(items), "corpus": len(corpus),
                                  "mapped": len(fresh), "after_merge": len(merged),
                                  "reasons": dict(reasons)},
                                 indent=1, sort_keys=True), encoding="utf-8")
    print("wrote %s and %s" % (OUT.name, REPORT.name))


if __name__ == "__main__":
    main()
