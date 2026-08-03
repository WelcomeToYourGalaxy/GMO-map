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
    """Normalise for matching, keeping every script. The old version stripped
    anything non-ASCII, which erased Chinese, Japanese, Korean, Cyrillic, Thai,
    Devanagari, Bengali and Arabic headlines down to punctuation \u2014 and then
    matched short Latin fragments against the remains, tagging them all as the
    United States. Accents are folded; letters are kept."""
    s = unicodedata.normalize("NFD", str(s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c if (c.isalnum() or c.isspace()) else " " for c in s).strip()


def _has_name(hay, name):
    """Word-boundary match for space-delimited scripts, plain substring for the
    ones that do not use spaces. Chinese and Japanese headlines have no spaces
    around a country name, so a boundary test can never fire on them."""
    if _scriptless(name):
        return name in hay
    return (" " + name + " ") in hay


# Scripts written without spaces between words. A word-boundary test can never
# fire on these, so they are matched as plain substrings instead.
_NOSPACE = ((0x0E00, 0x0E7F),   # Thai
            (0x0E80, 0x0EFF),   # Lao
            (0x1000, 0x109F),   # Myanmar
            (0x1780, 0x17FF),   # Khmer
            (0x2E80, 0x9FFF),   # CJK radicals through unified ideographs
            (0x3040, 0x30FF),   # kana
            (0xAC00, 0xD7AF))   # hangul syllables


def _scriptless(name):
    for c in name:
        o = ord(c)
        for lo, hi in _NOSPACE:
            if lo <= o <= hi:
                return True
    return False



# --- native and localised country names --------------------------------------
# The table above is English-only, which is why every non-English feed landed
# untagged and the region dropdown read zero: "Deutschland" does not match
# "Germany" and "\u4e2d\u56fd" does not match "China". The wire queries in twenty
# languages; the names have to exist in those languages too.
NATIVE_NAMES = {
 "DEU": ["Deutschland", "Alemania", "Allemagne", "Germania", "Alemanha", "\u5fb7\u56fd", "\u30c9\u30a4\u30c4", "Almanya", "\u0413\u0435\u0440\u043c\u0430\u043d\u0438\u044f", "Duitsland", "Niemcy", "Tyskland"],
 "FRA": ["Frankreich", "Francia", "Fran\u00e7a", "\u6cd5\u56fd", "\u30d5\u30e9\u30f3\u30b9", "Fransa", "\u0424\u0440\u0430\u043d\u0446\u0438\u044f", "Frankrijk", "Francja", "Frankrike", "Pran\u00e7a"],
 "ESP": ["Espa\u00f1a", "Espagne", "Spanien", "Spagna", "Espanha", "\u897f\u73ed\u7259", "\u30b9\u30da\u30a4\u30f3", "\u0418\u0441\u043f\u0430\u043d\u0438\u044f", "Spanje", "Hiszpania"],
 "ITA": ["Italia", "Italie", "Italien", "It\u00e1lia", "\u610f\u5927\u5229", "\u30a4\u30bf\u30ea\u30a2", "\u0418\u0442\u0430\u043b\u0438\u044f", "Itali\u00eb", "W\u0142ochy"],
 "BRA": ["Brasil", "Br\u00e9sil", "Brasilien", "Brasile", "\u5df4\u897f", "\u30d6\u30e9\u30b8\u30eb", "\u0411\u0440\u0430\u0437\u0438\u043b\u0438\u044f", "Brazylia", "Brezilya"],
 "MEX": ["M\u00e9xico", "Mexique", "Mexiko", "Messico", "\u58a8\u897f\u54e5", "\u30e1\u30ad\u30b7\u30b3", "\u041c\u0435\u043a\u0441\u0438\u043a\u0430", "Meksyk"],
 "ARG": ["Argentine", "Argentinien", "\u963f\u6839\u5ef7", "\u30a2\u30eb\u30bc\u30f3\u30c1\u30f3", "\u0410\u0440\u0433\u0435\u043d\u0442\u0438\u043d\u0430", "Argentini\u00eb", "Arjantin"],
 "CHN": ["\u4e2d\u56fd", "\u4e2d\u570b", "China", "Chine", "Cina", "\u4e2d\u83ef", "\u4e2d\u56fd\u5927\u9646", "\u0e08\u0e35\u0e19", "\u0915\u094d\u200d\u092f\u093e", "\u041a\u0438\u0442\u0430\u0439", "\u30c1\u30e3\u30a4\u30ca", "\u4e2d\u56fd\u653f\u5e9c", "\u0e08\u0e35\u0e19", "\u4e2d\u56fd", "\u0645\u0627\u0644\u0635\u064a\u0646"],
 "JPN": ["\u65e5\u672c", "Jap\u00f3n", "Japon", "Japan", "Giappone", "\u30cb\u30db\u30f3", "\u0414\u0436\u0430\u043f\u043e\u043d", "\u65e5\u672c\u653f\u5e9c", "Japonia", "Japonya"],
 "KOR": ["\ud55c\uad6d", "\ub300\ud55c\ubbfc\uad6d", "Corea", "Cor\u00e9e", "Korea", "\u97e9\u56fd", "Kore"],
 "IND": ["\u092d\u093e\u0930\u0924", "India", "Inde", "Indien", "\u5370\u5ea6", "\u30a4\u30f3\u30c9", "\u0418\u043d\u0434\u0438\u044f", "Hindistan", "Indie"],
 "RUS": ["\u0420\u043e\u0441\u0441\u0438\u0438", "\u0420\u043e\u0441\u0441\u0438\u044e", "\u0420\u043e\u0441\u0441\u0438\u0435\u0439", "\u0420\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u043e\u0439", "\u0420\u043e\u0441\u0441\u0438\u044f", "Russie", "Russland", "Rusia", "R\u00fassia", "\u4fc4\u7f57\u65af", "\u30ed\u30b7\u30a2", "Rusya", "Rosja"],
 "TUR": ["T\u00fcrkiye", "Turquie", "T\u00fcrkei", "Turqu\u00eda", "\u571f\u8033\u5176", "\u30c8\u30eb\u30b3", "\u0422\u0443\u0440\u0446\u0438\u044f"],
 "USA": ["Estados Unidos", "\u00c9tats-Unis", "Vereinigte Staaten", "Stati Uniti", "\u7f8e\u56fd", "\u30a2\u30e1\u30ea\u30ab", "\u0421\u0428\u0410", "\u0623\u0645\u0631\u064a\u0643\u0627", "Amerika Birle\u015fik", "EE.UU.", "EEUU"],
 "GBR": ["Reino Unido", "Royaume-Uni", "Gro\u00dfbritannien", "Regno Unito", "\u82f1\u56fd", "\u30a4\u30ae\u30ea\u30b9", "\u0412\u0435\u043b\u0438\u043a\u043e\u0431\u0440\u0438\u0442\u0430\u043d\u0438\u044f"],
 "NLD": ["Nederland", "Pa\u00edses Bajos", "Pays-Bas", "Niederlande", "Paesi Bassi", "\u8377\u5170", "Holanda", "Holandia"],
 "POL": ["Polsce", "Polski", "Polsk\u0105", "Polska", "Pologne", "Polen", "Polonia", "Pol\u00f4nia", "\u6ce2\u5170", "\u041f\u043e\u043b\u044c\u0448\u0430"],
 "SWE": ["Sverige", "Su\u00e8de", "Schweden", "Suecia", "Svezia", "\u745e\u5178", "\u0428\u0432\u0435\u0446\u0438\u044f", "Szwecja"],
 "ROU": ["Rom\u00e2niei", "Rom\u00e2nia", "Roumanie", "Rum\u00e4nien", "Ruman\u00eda", "Romania", "\u7f57\u9a6c\u5c3c\u4e9a"],
 "PRT": ["Portugal", "Portogallo", "\u8461\u8404\u7259", "\u041f\u043e\u0440\u0442\u0443\u0433\u0430\u043b\u0438\u044f", "Portekiz"],
 "AUT": ["\u00d6sterreich", "Autriche", "Austria", "\u5967\u5730\u5229", "\u5967\u5730\u5229", "\u0410\u0432\u0441\u0442\u0440\u0438\u044f", "Avusturya"],
 "CHE": ["Schweiz", "Suisse", "Suiza", "Svizzera", "Su\u00ed\u00e7a", "\u745e\u58eb", "\u0428\u0432\u0435\u0439\u0446\u0430\u0440\u0438\u044f", "\u0130svi\u00e7re"],
 "UKR": ["\u0423\u043a\u0440\u0430\u0457\u043d\u0456", "\u0423\u043a\u0440\u0430\u0438\u043d\u0435", "\u0423\u043a\u0440\u0430\u0438\u043d\u044b", "\u0423\u043a\u0440\u0430\u0457\u043d\u0438", "\u0423\u043a\u0440\u0430\u0457\u043d\u0430", "\u0423\u043a\u0440\u0430\u0438\u043d\u0430", "Ukraine", "Ucrania", "Ucraina", "\u4e4c\u514b\u5170", "Ukrayna"],
 "IDN": ["Indonesia", "Indon\u00e9sie", "Indonesien", "\u5370\u5ea6\u5c3c\u897f\u4e9a", "\u0625\u0646\u062f\u0648\u0646\u064a\u0633\u064a\u0627"],
 "MYS": ["Malaysia", "Malaisie", "Malasia", "\u9a6c\u6765\u897f\u4e9a", "\u30de\u30ec\u30fc\u30b7\u30a2"],
 "THA": ["\u0e1b\u0e23\u0e30\u0e40\u0e17\u0e28\u0e44\u0e17\u0e22", "\u0e44\u0e17\u0e22", "Thailand", "Tha\u00eflande", "Tailandia", "\u6cf0\u56fd"],
 "VNM": ["Vi\u1ec7t Nam", "Vietnam", "Vi\u00eatnam", "\u8d8a\u5357", "\u30d9\u30c8\u30ca\u30e0"],
 "EGY": ["\u0645\u0635\u0631", "Egipto", "\u00c9gypte", "\u00c4gypten", "Egitto", "\u57c3\u53ca", "M\u0131s\u0131r"],
 "MAR": ["\u0627\u0644\u0645\u063a\u0631\u0628", "Marruecos", "Maroc", "Marokko", "Marocco", "\u6469\u6d1b\u54e5", "Fas"],
 "SAU": ["\u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629", "Arabia Saudita", "Arabie saoudite", "Saudi-Arabien", "\u6c99\u7279"],
 "ZAF": ["Sud\u00e1frica", "Afrique du Sud", "S\u00fcdafrika", "Sudafrica", "\u00c1frica do Sul", "\u5357\u975e", "G\u00fcney Afrika"],
 "NGA": ["Nigeria", "Nig\u00e9ria", "\u5c3c\u65e5\u5229\u4e9a", "\u0646\u064a\u062c\u064a\u0631\u064a\u0627"],
 "KEN": ["Kenia", "K\u00e9nya", "Kenya", "\u80af\u5c3c\u4e9a", "\u0643\u064a\u0646\u064a\u0627"],
 "CAN": ["Canad\u00e1", "Kanada", "Canada", "\u52a0\u62ff\u5927", "\u30ab\u30ca\u30c0", "\u041a\u0430\u043d\u0430\u0434\u0430"],
 "AUS": ["Australie", "Australien", "Austr\u00e1lia", "\u6fb3\u5927\u5229\u4e9a", "\u30aa\u30fc\u30b9\u30c8\u30e9\u30ea\u30a2", "Avustralya"],
 "NZL": ["Nueva Zelanda", "Nouvelle-Z\u00e9lande", "Neuseeland", "\u65b0\u897f\u5170", "\u30cb\u30e5\u30fc\u30b8\u30fc\u30e9\u30f3\u30c9"],
 "COL": ["Colombie", "Kolumbien", "Col\u00f4mbia", "\u54e5\u4f26\u6bd4\u4e9a"],
 "CHL": ["Chili", "Chile", "Cile", "\u667a\u5229"],
 "PER": ["P\u00e9rou", "Peru", "Per\u00fa", "\u79d8\u9c81"],
 "PRY": ["Paraguay", "Paraguai", "\u5df4\u62c9\u572d"],
 "URY": ["Uruguay", "Uruguai", "\u4e4c\u62c9\u572d"],
 "BOL": ["Bolivie", "Bolivien", "Bol\u00edvia", "\u73bb\u5229\u7ef4\u4e9a"],
 "ECU": ["\u00c9quateur", "Ecuador", "Equador", "\u5384\u74dc\u591a\u5c14"],
 "CUB": ["Cuba", "Kuba", "\u53e4\u5df4"],
 "ISR": ["Israel", "Isra\u00ebl", "Israele", "\u4ee5\u8272\u5217", "\u0625\u0633\u0631\u0627\u0626\u064a\u0644"],
 "PAK": ["Pakist\u00e1n", "Pakistan", "\u5df4\u57fa\u65af\u5766", "\u092a\u093e\u0915\u093f\u0938\u094d\u0924\u093e\u0928", "\u0628\u0627\u0643\u0633\u062a\u0627\u0646"],
 "BGD": ["Bangladesh", "\u09ac\u09be\u0982\u09b2\u09be\u09a6\u09c7\u09b6", "\u5b5f\u52a0\u62c9\u56fd"],
 "PHL": ["Filipinas", "Philippines", "Philippinen", "\u83f2\u5f8b\u5bbe"],
 "SGP": ["Singapur", "Singapour", "Singapore", "\u65b0\u52a0\u5761"],
 "TWN": ["\u53f0\u7063", "\u53f0\u6e7e", "Taiwan", "Taiw\u00e1n"],
 "DNK": ["Danmark", "Dinamarca", "Danemark", "D\u00e4nemark", "\u4e39\u9ea6"],
 "NOR": ["Norge", "Noruega", "Norv\u00e8ge", "Norwegen", "\u632a\u5a01"],
 "FIN": ["Suomi", "Finlandia", "Finlande", "Finnland", "\u82ac\u5170"],
 "IRL": ["Irlanda", "Irlande", "Irland", "\u7231\u5c14\u5170"],
 "GRC": ["\u0395\u03bb\u03bb\u03ac\u03b4\u03b1", "\u0395\u03bb\u03bb\u03ac\u03b4\u03b1\u03c2", "Grecia", "Gr\u00e8ce", "Griechenland", "\u5e0c\u814a", "Yunanistan"],
 "HUN": ["Magyarorsz\u00e1gon", "Magyarorsz\u00e1g", "Hungr\u00eda", "Hongrie", "Ungarn", "\u5308\u7259\u5229"],
 "CZE": ["\u010cesku", "\u010cesk\u00e9", "\u010cesko", "\u010cesk\u00e1 republika", "Chequia", "Tch\u00e9quie", "Tschechien", "\u6377\u514b"],
 "ETH": ["Etiop\u00eda", "\u00c9thiopie", "\u00c4thiopien", "\u57c3\u585e\u4fc4\u6bd4\u4e9a"],
 "GHA": ["Ghana", "\u52a0\u7eb3"],
 "TZA": ["Tanzania", "Tanzanie", "Tansania", "\u5766\u6851\u5c3c\u4e9a"],
 "ZMB": ["Zambia", "Zambie", "Sambia", "\u8d5e\u6bd4\u4e9a"],
 "CRI": ["Costa Rica", "\u54e5\u65af\u8fbe\u9ece\u52a0"],
 "ARE": ["Emiratos", "\u00c9mirats", "\u0627\u0644\u0625\u0645\u0627\u0631\u0627\u062a", "\u963f\u8054\u914b"],
 "KAZ": ["Kazajist\u00e1n", "Kazakhstan", "Kasachstan", "\u54c8\u8428\u514b\u65af\u5766", "\u041a\u0430\u0437\u0430\u0445\u0441\u0442\u0430\u043d"],
}
for _iso, _names in NATIVE_NAMES.items():
    COUNTRIES.setdefault(_iso, [])
    for _n in _names:
        if _n not in COUNTRIES[_iso]:
            COUNTRIES[_iso].append(_n)

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
            if _has_name(hay, name):
                item["iso"] = iso
                break
    if not item.get("iso"):
        for name, iso2 in _SUB2ISO:
            if _has_name(hay, name):
                item["iso"] = iso2
                break
    iso = item.get("iso")
    if iso and not item.get("region") and iso in _SUBS:
        full = " " + slug((item.get("title") or "") + " " + (item.get("snippet") or "")) + " "
        for name, canon in _SUBS[iso]:
            if _has_name(full, name):
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
    # Google News queries carry their own language in hl=; trust that over the
    # feed's <language> element, which those endpoints do not always set.
    m = re.search(r"[?&]hl=([a-zA-Z]{2})", url)
    if m:
        FEED_LANG[name] = m.group(1).lower()
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
