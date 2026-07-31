#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harvest the wire feeds into wire.json, geo-tagged and language-tagged.

Why the tagging happens here rather than in the browser: index.html can tag at
render time, but that path has failed repeatedly and is hard to inspect from
outside. Tagging in the harvester means wire.json ships with `iso`, `region` and
`lang` already populated, the region dropdown counts come straight from the
data, and the output can be checked before it is committed.

    python3 harvest/wire_harvest.py            # harvest and write wire.json
    python3 harvest/wire_harvest.py --selftest # tag a sample, print, write nothing

Standard library only.
"""
import json, re, sys, html, hashlib, pathlib, unicodedata
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from email.utils import parsedate_to_datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
OUT = ROOT / "wire.json"

KEEP_DAYS = 120
MAX_ITEMS = 4000
TIMEOUT = 25
UA = ("Mozilla/5.0 (compatible; GMO-map wire harvester; "
      "+https://github.com/WelcomeToYourGalaxy/GMO-map)")

# ---------------------------------------------------------------- geo tables --
COUNTRIES = {
 "USA": ["united states", "u s a", "america", "american", "usda", "aphis"],
 "CAN": ["canada", "canadian"], "MEX": ["mexico", "mexican"],
 "BRA": ["brazil", "brazilian"], "ARG": ["argentina", "argentine", "argentinian"],
 "CHL": ["chile", "chilean"], "COL": ["colombia", "colombian"], "PER": ["peru", "peruvian"],
 "URY": ["uruguay"], "PRY": ["paraguay"], "BOL": ["bolivia"], "ECU": ["ecuador"],
 "VEN": ["venezuela"], "CRI": ["costa rica"], "GTM": ["guatemala"], "HND": ["honduras"],
 "PAN": ["panama"], "CUB": ["cuba"], "DOM": ["dominican republic"],
 "GBR": ["united kingdom", "britain", "england", "scotland", "wales", "northern ireland", "british"],
 "IRL": ["ireland", "irish"], "FRA": ["france", "french"], "DEU": ["germany", "german"],
 "ESP": ["spain", "spanish"], "PRT": ["portugal", "portuguese"], "ITA": ["italy", "italian"],
 "NLD": ["netherlands", "holland", "dutch"], "BEL": ["belgium", "belgian"],
 "AUT": ["austria", "austrian"], "CHE": ["switzerland", "swiss"], "POL": ["poland", "polish"],
 "CZE": ["czechia", "czech republic", "czech"], "SVK": ["slovakia"], "HUN": ["hungary", "hungarian"],
 "ROU": ["romania", "romanian"], "BGR": ["bulgaria"], "HRV": ["croatia"], "SVN": ["slovenia"],
 "SRB": ["serbia"], "GRC": ["greece", "greek"], "SWE": ["sweden", "swedish"],
 "NOR": ["norway", "norwegian"], "DNK": ["denmark", "danish"], "FIN": ["finland", "finnish"],
 "ISL": ["iceland"], "EST": ["estonia"], "LVA": ["latvia"], "LTU": ["lithuania"],
 "UKR": ["ukraine", "ukrainian"], "RUS": ["russia", "russian"], "TUR": ["turkiye", "turkey", "turkish"],
 "IND": ["india", "indian"], "PAK": ["pakistan"], "BGD": ["bangladesh"], "LKA": ["sri lanka"],
 "NPL": ["nepal"], "CHN": ["china", "chinese"], "JPN": ["japan", "japanese"],
 "KOR": ["south korea", "korea", "korean"], "TWN": ["taiwan", "taiwanese"],
 "PHL": ["philippines", "filipino"], "VNM": ["viet nam", "vietnam", "vietnamese"],
 "THA": ["thailand", "thai"], "MYS": ["malaysia", "malaysian"], "IDN": ["indonesia", "indonesian"],
 "MMR": ["myanmar", "burma"], "KHM": ["cambodia"], "LAO": ["laos"],
 "AUS": ["australia", "australian"], "NZL": ["new zealand"],
 "ZAF": ["south africa", "south african"], "KEN": ["kenya", "kenyan"],
 "NGA": ["nigeria", "nigerian"], "GHA": ["ghana", "ghanaian"], "UGA": ["uganda", "ugandan"],
 "TZA": ["tanzania"], "ETH": ["ethiopia", "ethiopian"], "ZMB": ["zambia", "zambian"],
 "ZWE": ["zimbabwe"], "MWI": ["malawi"], "MOZ": ["mozambique"], "BFA": ["burkina faso"],
 "MLI": ["mali"], "SEN": ["senegal"], "CMR": ["cameroon"], "SDN": ["sudan"],
 "EGY": ["egypt", "egyptian"], "MAR": ["morocco"], "TUN": ["tunisia"], "DZA": ["algeria"],
 "ISR": ["israel", "israeli"], "SAU": ["saudi arabia"], "ARE": ["united arab emirates"],
 "IRN": ["iran", "iranian"], "IRQ": ["iraq"],
}

SUBREGIONS = {
 "USA": ["california","texas","iowa","nebraska","kansas","illinois","indiana","ohio","minnesota",
         "missouri","arkansas","mississippi","louisiana","florida","georgia","north carolina",
         "south carolina","virginia","new york","pennsylvania","michigan","wisconsin","oregon",
         "washington","idaho","montana","colorado","arizona","new mexico","hawaii","alaska",
         "north dakota","south dakota","oklahoma","kentucky","tennessee","alabama","maine","vermont"],
 "BRA": ["mato grosso","parana","rio grande do sul","goias","bahia","minas gerais","sao paulo",
         "para","amazonas","santa catarina","mato grosso do sul","maranhao","piaui","tocantins"],
 "ARG": ["buenos aires","cordoba","santa fe","entre rios","chaco","salta","tucuman","misiones"],
 "IND": ["maharashtra","gujarat","punjab","haryana","karnataka","tamil nadu","andhra pradesh",
         "telangana","madhya pradesh","uttar pradesh","bihar","west bengal","odisha","rajasthan",
         "kerala","assam","chhattisgarh","jharkhand"],
 "AUS": ["new south wales","victoria","queensland","south australia","western australia",
         "tasmania","northern territory"],
 "CAN": ["ontario","quebec","alberta","saskatchewan","manitoba","british columbia",
         "nova scotia","new brunswick","prince edward island","newfoundland"],
 "MEX": ["oaxaca","chiapas","sinaloa","sonora","jalisco","michoacan","veracruz","puebla",
         "guanajuato","yucatan","campeche","chihuahua","tamaulipas"],
 "DEU": ["bavaria","bayern","saxony","sachsen","brandenburg","lower saxony","niedersachsen",
         "baden wurttemberg","hesse","hessen","thuringia","mecklenburg"],
 "ESP": ["aragon","catalonia","catalunya","andalusia","extremadura","castilla la mancha",
         "castilla y leon","navarre","valencia","galicia"],
 "ZAF": ["gauteng","free state","mpumalanga","limpopo","kwazulu natal","western cape",
         "eastern cape","northern cape","north west"],
 "CHN": ["heilongjiang","jilin","xinjiang","henan","shandong","hebei","anhui","hubei","hunan",
         "sichuan","yunnan","guangdong","inner mongolia"],
 "PHL": ["luzon","mindanao","visayas","isabela","nueva ecija","laguna","bukidnon","iloilo"],
 "NGA": ["kano","kaduna","lagos","abuja","borno","oyo","benue","plateau"],
 "KEN": ["nairobi","kisumu","mombasa","nakuru","eldoret","machakos"],
 "PAK": ["punjab","sindh","balochistan","khyber pakhtunkhwa"],
 "JPN": ["hokkaido","honshu","kyushu","okinawa","tokyo","osaka","hiroshima"],
}

FEED_LANG = {}

_slug_rx = re.compile(r"[^a-z0-9]+")


def slug(s):
    s = unicodedata.normalize("NFD", str(s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return _slug_rx.sub(" ", s).strip()


_NAMES = sorted(((slug(n), iso) for iso, names in COUNTRIES.items() for n in names),
                key=lambda x: -len(x[0]))
_SUBS = {iso: sorted(((slug(r), r) for r in rs), key=lambda x: -len(x[0]))
         for iso, rs in SUBREGIONS.items()}

# Subregion names that belong to exactly one country can imply the country when
# the headline never names it - "Oregon bentgrass ... USDA says" is a US story.
# Ambiguous names (Georgia, Victoria, Punjab, Washington, Para) are excluded.
_AMBIG = set()
_seen_sub = {}
for _iso, _rs in SUBREGIONS.items():
    for _r in _rs:
        _k = slug(_r)
        if _k in _seen_sub and _seen_sub[_k] != _iso:
            _AMBIG.add(_k)
        _seen_sub[_k] = _iso
for _k in ("georgia", "victoria", "washington", "para", "cordoba", "valencia", "new york"):
    _AMBIG.add(_k)
_SUB2ISO = sorted(((k, v) for k, v in _seen_sub.items()
                   if k not in _AMBIG and len(k) >= 5), key=lambda x: -len(x[0]))


def geotag(item):
    """Set iso and region from the headline. Title only for the country, because
    body text name-drops far too many countries to tag on."""
    hay = " " + slug(item.get("title")) + " "
    if not item.get("iso"):
        for name, iso in _NAMES:
            if " " + name + " " in hay:
                item["iso"] = iso
                break
    if not item.get("iso"):
        for name, iso2 in _SUB2ISO:
            if " " + name + " " in hay:
                item["iso"] = iso2
                break
    iso = item.get("iso")
    if iso and not item.get("region") and iso in _SUBS:
        full = " " + slug((item.get("title") or "") + " " + (item.get("snippet") or "")) + " "
        for name, canon in _SUBS[iso]:
            if " " + name + " " in full:
                item["region"] = canon.title()
                break
    return item


# ------------------------------------------------------------------- fetch ----
def feeds_from_index():
    src = INDEX.read_text(encoding="utf-8")
    m = re.search(r"const WIRE_FEEDS\s*=\s*(\[.*?\]);", src, re.S)
    if not m:
        sys.exit("WIRE_FEEDS not found in index.html")
    return json.loads(m.group(1))


def fetch(url):
    req = Request(url, headers={"User-Agent": UA,
                                "Accept": "application/rss+xml, application/xml, text/xml, */*"})
    with urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def strip(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


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
        m = re.search(r'<%s[^>]*href=["\']([^"\']+)["\']' % n, block, re.I)
        if m:
            return m.group(1)
    return ""


def parse_feed(name, xml):
    lang = FEED_LANG.get(name)
    if not lang:
        m = re.search(r"<language[^>]*>([a-zA-Z\-]{2,7})</language>", xml, re.I)
        lang = (m.group(1).split("-")[0].lower() if m else "en")
    out = []
    blocks = (re.findall(r"<item[\s>].*?</item>", xml, re.S | re.I)
              or re.findall(r"<entry[\s>].*?</entry>", xml, re.S | re.I))
    for b in blocks:
        title, link = strip(tag(b, "title")), strip(tag(b, "link", "id"))
        if not title or not link:
            continue
        d = parse_date(strip(tag(b, "pubDate", "published", "updated", "dc:date"))) \
            or datetime.now(timezone.utc)
        out.append(geotag({
            "name": name, "title": title[:400], "link": link,
            "date": d.astimezone(timezone.utc).isoformat(),
            "snippet": strip(tag(b, "description", "summary", "content"))[:500],
            "iso": "", "region": "", "lang": lang, "sig": 0,
        }))
    return out


def one(entry):
    name, url = entry[0], entry[1]
    try:
        return parse_feed(name, fetch(url))
    except (URLError, HTTPError, TimeoutError, OSError) as e:
        print("  ! %-42s %s" % (name, e), file=sys.stderr)
        return []


def selftest():
    sample = ["Brazil approves new GM maize for cultivation in Mato Grosso",
              "India: GEAC clears field trials in Maharashtra",
              "Kenya lifts GMO import ban after court ruling",
              "Gene-edited crop rules relaxed across Germany",
              "Bayer faces new lawsuit over seed patents",
              "Philippines court reinstates Golden Rice permit",
              "Contamination found in Hokkaido canola survey, Japan",
              "EU parliament votes on new genomic techniques",
              "Argentina approves HB4 wheat for Buenos Aires province",
              "Oregon bentgrass escape still not eradicated, USDA says"]
    tagged = 0
    for s in sample:
        it = geotag({"title": s, "snippet": "", "iso": "", "region": ""})
        tagged += 1 if it["iso"] else 0
        print("  %-5s %-16s %s" % (it["iso"] or "--", it["region"] or "-", s[:54]))
    print("country-tagged %d/%d" % (tagged, len(sample)))
    print("country name forms %d | subregion tables %d" % (len(_NAMES), len(_SUBS)))


def main():
    if "--selftest" in sys.argv:
        selftest(); return
    feeds = feeds_from_index()
    print("harvesting %d feeds" % len(feeds))
    items = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for got in ex.map(one, feeds):
            items.extend(got)
    print("  fetched %d items" % len(items))

    if OUT.exists():
        try:
            items.extend(geotag(x) for x in (json.loads(OUT.read_text(encoding="utf-8")) or []))
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

    iso_n = sum(1 for x in merged if x.get("iso"))
    reg_n = sum(1 for x in merged if x.get("region"))
    langs = sorted({x.get("lang", "en") for x in merged})
    print("wrote %s: %d items | %d country-tagged | %d subregion-tagged | langs: %s"
          % (OUT.name, len(merged), iso_n, reg_n, ",".join(langs)))
    if merged and iso_n == 0:
        print("  WARNING: nothing was country-tagged \u2014 the region filter will read 0",
              file=sys.stderr)


if __name__ == "__main__":
    main()
