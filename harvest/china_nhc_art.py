#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""China NHC — approved assisted reproduction institutions and sperm banks.

The National Health Commission publishes the full list of medical institutions
approved to perform assisted reproduction, and the separate list of approved
human sperm banks, updated roughly twice a year. The June 2025 edition names
635 reproductive centres. That is larger than the entire United States clinic
count, and none of it was on this map.

It is also a better register than most: every institution carries a street
address, the specific techniques it is approved for, and whether each of those
is in formal operation or still on trial. Approval is compulsory - performing
assisted reproduction without it is unlawful - so this is a register rather
than a membership list.

The lists arrive as .docx attachments to an NHC notice, so this reads files
rather than the web:

    harvest/nhc_docx/*.docx
    python3 harvest/china_nhc_art.py

Get them from the maternal and child health notices at
http://www.nhc.gov.cn/fys/s3581/new_list.shtml - search
经批准开展人类辅助生殖技术和设置人类精子库的医疗机构名单 for the current release.

TABLE SHAPE, read off the real file rather than assumed. Six columns:
province, number, institution, address, approved technique, operating status.
An institution approved for four techniques occupies four rows, with the first
four cells vertically merged and therefore EMPTY on every row after the first.
Reading each row as an institution would turn 635 centres into about 1,800.
"""

import json, re, sys, time, zipfile, pathlib
from urllib.request import Request, urlopen
from urllib.parse import quote

HERE = pathlib.Path(__file__).resolve().parent
INDIR = HERE / "nhc_docx"
OUT = HERE / "china_nhc_art.json"
CACHE = HERE / "_geocache.json"

PHOTON = "https://photon.komoot.io/api/?limit=1&lang=default&q="
SOURCE = "http://www.nhc.gov.cn/fys/s3581/new_list.shtml"

# Techniques, in the order the register lists them. Plain English, because a
# reader of this map is not assumed to read Chinese or to know the jargon.
TECH = [
    ("夫精人工授精", "insemination with the partner's sperm"),
    ("供精人工授精", "insemination with donor sperm"),
    ("常规体外受精-胚胎移植", "IVF with embryo transfer"),
    ("体外受精-胚胎移植", "IVF with embryo transfer"),
    ("卵胞浆内单精子显微注射", "ICSI \u2014 a single sperm injected into the egg"),
    ("植入前胚胎遗传学诊断", "embryo screening before transfer"),
    ("植入前胚胎遗传学检测", "embryo screening before transfer"),
]

# Province centroids, for an address that will not geocode. Chinese addresses
# defeat most geocoders, and a province centroid that says it is one is better
# than a street-level guess that is wrong.
PROVINCE = {
    "北京": (39.90, 116.41), "天津": (39.13, 117.20), "河北": (38.04, 114.53),
    "山西": (37.87, 112.55), "内蒙古": (40.82, 111.75), "辽宁": (41.80, 123.43),
    "吉林": (43.90, 125.33), "黑龙江": (45.80, 126.53), "上海": (31.23, 121.47),
    "江苏": (32.06, 118.80), "浙江": (30.27, 120.15), "安徽": (31.86, 117.28),
    "福建": (26.08, 119.30), "江西": (28.68, 115.89), "山东": (36.68, 117.02),
    "河南": (34.76, 113.65), "湖北": (30.55, 114.34), "湖南": (28.23, 112.94),
    "广东": (23.13, 113.27), "广西": (22.82, 108.32), "海南": (20.04, 110.20),
    "重庆": (29.56, 106.55), "四川": (30.57, 104.07), "贵州": (26.65, 106.63),
    "云南": (25.04, 102.72), "西藏": (29.65, 91.14), "陕西": (34.34, 108.94),
    "甘肃": (36.06, 103.83), "青海": (36.62, 101.78), "宁夏": (38.49, 106.23),
    "新疆": (43.79, 87.62), "兵团": (43.79, 87.62),
}


def get(url, tries=2):
    for i in range(tries):
        try:
            r = Request(url, headers={"User-Agent":
                                      "GMO-map/1.0 (public research map)"})
            return urlopen(r, timeout=60).read().decode("utf-8", "replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2)


# <w:t[^>]*> also matches <w:tcPr>, <w:tcW> and <w:tcBorders>, which pulled the
# whole cell-properties XML into the text of every cell. Require a space or an
# immediate close so only real text runs match.
_T = re.compile(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", re.S)
_TC = re.compile(r"<w:tc>(.*?)</w:tc>", re.S)
_TR = re.compile(r"<w:tr[\s>].*?</w:tr>", re.S)


def table_rows(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    out = []
    for tr in _TR.findall(x):
        cells = [re.sub(r"\s+", " ", "".join(_T.findall(tc))).strip()
                 for tc in _TC.findall(tr)]
        out.append(cells)
    return out


def institutions(rows):
    """One record per institution, gathering the merged technique rows.

    The two lists are not the same table. The reproductive-centre file has six
    columns and groups by province; the sperm-bank file has five and no province
    column at all, because there are 29 banks in the whole country and they are
    simply numbered. Reading both with the six-column rule found 635 centres and
    zero banks - a whole file silently producing nothing, which is the failure
    this project keeps having. The width decides which shape is being read.
    """
    width = max((len(c) for c in rows), default=0)
    if width == 5:
        recs, cur = [], None
        for c in rows:
            if len(c) < 5:
                continue
            num, name, addr, tech, state = (c + [""] * 5)[:5]
            if name in ("", "医疗机构名称"):
                if cur and tech:
                    cur["tech"].append((tech, state))
                continue
            if cur:
                recs.append(cur)
            cur = {"province": "", "no": num, "name": name,
                   "address": addr, "tech": ([(tech, state)] if tech else [])}
        if cur:
            recs.append(cur)
        return recs

    recs, cur = [], None
    province = ""
    for c in rows:
        if len(c) < 6:
            continue                      # title and count banners
        prov, num, name, addr, tech, state = (c + [""] * 6)[:6]
        if prov:
            province = prov
        if name:                          # a merge restart: a new institution
            if cur:
                recs.append(cur)
            cur = {"province": province, "no": num, "name": name,
                   "address": addr, "tech": []}
        if cur and tech:
            cur["tech"].append((tech, state))
    if cur:
        recs.append(cur)
    return [r for r in recs if r["name"] and r["name"] != "医疗机构名称"]


def load_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def geocode(addr, cache):
    if addr in cache:
        return cache[addr]
    try:
        d = json.loads(get(PHOTON + quote(addr)))
        fs = d.get("features") or []
        if fs:
            c = fs[0]["geometry"]["coordinates"]
            cache[addr] = [round(c[1], 5), round(c[0], 5)]
            return cache[addr]
    except Exception:
        pass
    cache[addr] = None
    return None


def province_point(text):
    for k, v in PROVINCE.items():
        if k in text:
            return v, k
    return None, ""


def english_tech(t):
    for zh, en in TECH:
        if zh in t:
            return en
    return ""


def main():
    dry = "--dry-run" in sys.argv
    src = pathlib.Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else INDIR
    files = sorted(src.glob("*.docx")) if src.exists() else []
    if not files:
        print("No .docx in %s. Download the current lists from %s and put them "
              "there. Nothing written." % (src, SOURCE), file=sys.stderr)
        return

    cache = load_cache()
    out, exact_n, prov_n = [], 0, 0
    for f in files:
        # Decided on the table, not the filename. BOTH files are called
        # "...\u4eba\u7c7b\u7cbe\u5b50\u5e93..." because that phrase is in the
        # notice's title, so a filename test matched the centre list too and
        # skipped everything. The bank table has five columns and the centre
        # table six; that is a fact about the document rather than about what
        # somebody named the download.
        _rows = table_rows(f)
        bank = max((len(c) for c in _rows), default=0) == 5
        # China's 29 approved sperm banks are skipped. Not because they do not
        # matter, but because a bank stores gametes and a clinic decides what is
        # made from them: the selection, the screening and the transfer all
        # happen at the clinic. Mapping 29 Chinese banks while no other country's
        # banks are mapped as facilities would have made China look like the only
        # place they exist. The industry layer holds the large bank operators -
        # Cryos, European Sperm Bank, California Cryobank and others - as
        # organisations, which is the right level for a business whose product
        # travels.
        if bank:
            print("  sperm banks in this file: skipped, see the note in this "
                  "harvester")
            continue
        recs = institutions(_rows)
        print("  %-22s %d institutions" %
              ("sperm banks" if bank else "reproductive centres", len(recs)))
        for r in recs:
            pt, pname = province_point(r["province"] or r["address"])
            latlng = geocode(r["address"], cache) if r["address"] else None
            exact = latlng is not None
            if latlng is None:
                latlng = pt
            if latlng is None:
                continue
            exact_n += 1 if exact else 0
            prov_n += 0 if exact else 1

            techs = [english_tech(t) for t, _ in r["tech"]]
            techs = sorted(set([t for t in techs if t]))
            running = sum(1 for _, s in r["tech"] if "正式" in s)
            trial = sum(1 for _, s in r["tech"] if "试" in s)

            bits = ["A sperm bank approved by China's National Health Commission."
                    if bank else
                    "A medical institution approved by China's National Health "
                    "Commission to perform assisted reproduction."]
            if techs:
                bits.append("Approved for: %s." % "; ".join(techs))
            if trial:
                bits.append("%d of its approvals %s still on trial rather than in "
                            "formal operation." % (trial, "is" if trial == 1 else "are"))
            elif running:
                bits.append("All of its approvals are in formal operation.")
            if not bank:
                bits.append("A fertility clinic is where human embryos are made, selected and "
                "stored, and where assisted reproduction happens, like IVF, "
                "ICSI, egg and sperm donation, freezing embryos and eggs for "
                "later.")
            bits.append("Approval is compulsory in China and performing assisted "
                        "reproduction without it is unlawful, so this list is a "
                        "register rather than a directory of members. It names "
                        "every approved institution in the country, which is more "
                        "than almost any other state publishes.")
            if not exact:
                bits.append("The address did not geocode, so this point sits at "
                            "the centre of the province rather than at the "
                            "institution.")

            out.append({
                "name": r["name"][:150],
                "source": "industry:repro",
                "type": "Sperm bank" if bank else "Fertility clinic",
                "lat": latlng[0], "lng": latlng[1],
                "state": (r["province"] or pname) + ("" if not r["address"]
                                                     else " \u2014 " + r["address"][:80]),
                "precise": bool(exact),
                "addr_grade": ("operational" if exact else "centroid"),
                "impact": 2,
                "company": "", "size": ("%d approved techniques" % len(r["tech"])
                                        if r["tech"] else ""),
                "status": ("Approved \u2014 %d in operation, %d on trial"
                           % (running, trial)) if r["tech"] else "Approved",
                "phase": "post", "date": "",
                "otype": "institute",
                "tags": ["repro:banks" if bank else "repro:clinics"],
                "species": ["human"],
                "url": SOURCE,
                "desc": " ".join(bits),
                "checked": "",
            })
            if len(out) % 40 == 0:
                time.sleep(0.6)

    print("  %d records: %d geocoded, %d at a province centroid"
          % (len(out), exact_n, prov_n))
    if not out:
        print("  nothing parsed \u2014 the table shape has changed. Nothing "
              "written; check institutions().", file=sys.stderr)
        return
    if dry:
        print("dry run \u2014 nothing written")
        return
    CACHE.write_text(json.dumps(cache, indent=0), encoding="utf-8")
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("Institutions approved to perform assisted reproduction, and "
                 "approved human sperm banks, from China's National Health "
                 "Commission. Approval is compulsory, so this is a register."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d records" % (OUT.name, len(out)))


if __name__ == "__main__":
    main()
