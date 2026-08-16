#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""India's National ART and Surrogacy Registry — 4,527 registered clinics.

Registration under the Assisted Reproductive Technology (Regulation) Act 2021 is
compulsory: a clinic operating without it is committing an offence. So this is a
register, not a directory, and at roughly 4,500 clinics it is the largest single
source of fertility facilities anywhere — an order of magnitude above the United
States. Each row carries a name, a street address, a state, an email and a
registration number, which makes these operational addresses rather than the
head offices most registers hand out.

WHY THIS PROBES RATHER THAN ASKS.

The listing is a DataTables grid showing ten rows at a time. The site's
datatables.init.js is stock demo boilerplate with no ajax configuration in it,
and the page carries no inline script, so nothing published says where the rows
come from. Rather than keep asking somebody to read a Network tab, this tries
the handful of shapes such a page can have, uses whichever returns clinic rows,
and prints which one worked. If none do, it says so and writes nothing.

    python3 harvest/india_nartsr.py
    python3 harvest/india_nartsr.py --dry-run
    python3 harvest/india_nartsr.py --from-file page.htm   # one saved page
"""

import json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "india_nartsr.json"
CACHE = HERE / "_geocache.json"

BASE = "https://registry.artsurrogacy.gov.in"
LIST = BASE + "/clinic/list?type=register-clinic"
PHOTON = "https://photon.komoot.io/api/?limit=1&q="

# Indian state and union territory centres, for a row whose address will not
# resolve. Every row carries a state, so nothing needs to fall back further.
STATE = {
    "ANDHRA PRADESH": (15.91, 79.74), "ARUNACHAL PRADESH": (28.22, 94.73),
    "ASSAM": (26.20, 92.94), "BIHAR": (25.10, 85.31), "CHANDIGARH": (30.73, 76.78),
    "CHHATTISGARH": (21.28, 81.87), "DELHI": (28.70, 77.10), "GOA": (15.30, 74.12),
    "GUJARAT": (22.26, 71.19), "HARYANA": (29.06, 76.09),
    "HIMACHAL PRADESH": (31.10, 77.17), "JAMMU AND KASHMIR": (33.78, 76.58),
    "JHARKHAND": (23.61, 85.28), "KARNATAKA": (15.32, 75.71),
    "KERALA": (10.85, 76.27), "LADAKH": (34.15, 77.58),
    "MADHYA PRADESH": (22.97, 78.66), "MAHARASHTRA": (19.75, 75.71),
    "MANIPUR": (24.66, 93.91), "MEGHALAYA": (25.47, 91.37),
    "MIZORAM": (23.16, 92.94), "NAGALAND": (26.16, 94.56),
    "ODISHA": (20.95, 85.10), "PUDUCHERRY": (11.94, 79.81),
    "PUNJAB": (31.15, 75.34), "RAJASTHAN": (27.02, 74.22),
    "SIKKIM": (27.53, 88.51), "TAMIL NADU": (11.13, 78.66),
    "TELANGANA": (18.11, 79.02), "TRIPURA": (23.94, 91.99),
    "UTTAR PRADESH": (26.85, 80.95), "UTTARAKHAND": (30.07, 79.09),
    "WEST BENGAL": (22.99, 87.85), "ANDAMAN AND NICOBAR ISLANDS": (11.74, 92.66),
    "DADRA AND NAGAR HAVELI AND DAMAN AND DIU": (20.40, 72.83),
    "LAKSHADWEEP": (10.57, 72.64),
}


def fetch(url, data=None, headers=None, tries=1, timeout=25):
    h = {"User-Agent": "GMO-map/1.0 (public research map)",
         "X-Requested-With": "XMLHttpRequest",
         "Accept": "application/json, text/html, */*"}
    h.update(headers or {})
    for i in range(tries):
        try:
            req = Request(url, data=(urlencode(data).encode() if data else None),
                          headers=h)
            return urlopen(req, timeout=timeout).read().decode("utf-8", "replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(3)


def _text(s):
    import html as _h
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def rows_from_html(html):
    """Rows out of the listing table. The header names the columns, so the
    positions are read rather than assumed - the registry has changed column
    order between releases before."""
    trs = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S)
    hdr, out = None, []
    for tr in trs:
        cells = [_text(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.S)]
        if not cells:
            continue
        if hdr is None and any("Clinic" in c for c in cells):
            hdr = [c.lower() for c in cells]
            continue
        if hdr is None or len(cells) < 4:
            continue
        def col(*names):
            for n in names:
                for i, h in enumerate(hdr):
                    if n in h and i < len(cells):
                        return cells[i]
            return ""
        name = col("name of the clinic", "clinic")
        if not name or name.isdigit():
            continue
        out.append({
            "name": name,
            "address": col("address"),
            "state": col("state"),
            # The registry obfuscates addresses as name[at]host[dot]com to slow
            # scrapers down. Restored, because a contact that cannot be written
            # to is not a contact.
            "email": col("email").replace("[at]", "@").replace("[dot]", "."),
            "reg": col("registration"),
        })
    return out


def rows_from_json(txt):
    try:
        d = json.loads(txt)
    except Exception:
        return []
    data = d.get("data") if isinstance(d, dict) else d
    if not isinstance(data, list) or not data:
        return []
    out = []
    for r in data:
        if isinstance(r, dict):
            g = lambda *k: next((str(r[x]) for x in k if r.get(x)), "")
            name = _text(g("clinic_name", "name", "name_of_clinic"))
            if not name:
                continue
            out.append({"name": name,
                        "address": _text(g("address", "clinic_address")),
                        "state": _text(g("state", "state_name")),
                        "email": _text(g("email", "email_id")).replace(
                            "[at]", "@").replace("[dot]", "."),
                        "reg": _text(g("registration_no", "reg_no", "registration"))})
        elif isinstance(r, list) and len(r) >= 5:
            out.append({"name": _text(str(r[1])), "address": _text(str(r[2])),
                        "state": _text(str(r[3])),
                        "email": _text(str(r[4])).replace("[at]", "@").replace(
                            "[dot]", "."),
                        "reg": _text(str(r[5])) if len(r) > 5 else ""})
    return out


def strategies(page, length=100):
    """Every shape this listing could plausibly have, cheapest first."""
    start = page * length
    return [
        ("laravel page=", LIST + "&page=%d" % (page + 1), None),
        ("datatables server-side",
         LIST + "&" + urlencode({"draw": 1, "start": start, "length": length}), None),
        ("datatables on /clinic/list-data",
         BASE + "/clinic/list-data?" + urlencode(
             {"type": "register-clinic", "draw": 1, "start": start,
              "length": length}), None),
        ("POST to the listing", LIST,
         {"draw": 1, "start": start, "length": length}),
    ]


def load_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def geocode(q, cache):
    if q in cache:
        return cache[q]
    try:
        d = json.loads(fetch(PHOTON + quote(q)))
        fs = d.get("features") or []
        if fs:
            c = fs[0]["geometry"]["coordinates"]
            cache[q] = [round(c[1], 5), round(c[0], 5)]
            return cache[q]
    except Exception:
        pass
    cache[q] = None
    return None


def harvest():
    """Find a working strategy on page 0, then use only that one."""
    if "--from-file" in sys.argv:
        html = pathlib.Path(sys.argv[sys.argv.index("--from-file") + 1]
                            ).read_text(encoding="utf-8", errors="replace")
        return rows_from_html(html), "a saved page"

    # A probe that hangs is worse than a probe that fails: the step gets killed
    # before it can report which shapes it tried. One attempt each, short
    # timeout, and the whole search is over in under two minutes.
    chosen, rows = None, []
    for label, url, post in strategies(0):
        try:
            txt = fetch(url, data=post)
        except Exception as e:
            print("  %-32s unreachable (%s)" % (label, e))
            continue
        got = rows_from_json(txt) or rows_from_html(txt)
        if len(got) > 10:
            print("  %-32s WORKS \u2014 %d rows" % (label, len(got)))
            chosen, rows = (label, url, post), got
            break
        print("  %-32s returned %d rows" % (label, len(got)))
    if not chosen:
        return [], None

    label, _, post = chosen
    seen = {r["reg"] or r["name"] for r in rows}
    started = time.time()
    for page in range(1, 60):
        if time.time() - started > 900:
            print("  fifteen minutes of paging; stopping with %d rows rather "
                  "than being killed with none" % len(rows))
            break
        _, url, p = strategies(page)[[s[0] for s in strategies(page)].index(label)]
        try:
            got = rows_from_json(fetch(url, data=p)) or rows_from_html(fetch(url, data=p))
        except Exception as e:
            print("  page %d failed (%s) \u2014 stopping here rather than "
                  "pretending the register ends" % (page, e))
            break
        fresh = [r for r in got if (r["reg"] or r["name"]) not in seen]
        if not fresh:
            break
        for r in fresh:
            seen.add(r["reg"] or r["name"])
        rows += fresh
        print("  page %d: %d rows (%d total)" % (page, len(fresh), len(rows)))
        time.sleep(1.5)
    return rows, label


def main():
    dry = "--dry-run" in sys.argv
    rows, how = harvest()
    if not rows:
        print("None of the listing shapes returned clinic rows. Nothing written.\n"
              "  Open %s, then DevTools > Network > Fetch/XHR, reload, and find the\n"
              "  request to registry.artsurrogacy.gov.in that carries the rows. Add\n"
              "  its URL to strategies()." % LIST, file=sys.stderr)
        return
    print("  %d clinics via %s" % (len(rows), how))

    cache = load_cache()
    out, exact_n = [], 0
    for r in rows:
        st = (r["state"] or "").upper().strip()
        latlng, exact = None, False
        if r["address"]:
            latlng = geocode("%s, %s, India" % (r["address"], st.title()), cache)
            exact = latlng is not None
        if latlng is None:
            latlng = STATE.get(st)
        if latlng is None:
            continue
        exact_n += 1 if exact else 0

        bits = ["A fertility clinic registered under India's Assisted Reproductive "
                "Technology (Regulation) Act 2021."]
        if r["reg"]:
            bits.append("Registration number %s." % r["reg"])
        bits.append("Registration is compulsory and operating without it is an "
                    "offence, so this is a register rather than a list of members. "
                    "It is also the largest of its kind anywhere: India records "
                    "several times as many clinics as the United States.")
        if not exact:
            bits.append("The address did not resolve, so this point sits at the "
                        "centre of the state rather than at the clinic.")

        out.append({
            "name": r["name"][:150], "source": "industry:repro",
            "type": "Fertility clinic",
            "lat": latlng[0], "lng": latlng[1],
            "state": ", ".join([x for x in (r["address"][:70], st.title()) if x]),
            "precise": bool(exact),
            "addr_grade": ("operational" if exact else "centroid"),
            "impact": 2, "company": "", "size": "",
            "status": "Registered under the ART Act",
            "phase": "post", "date": "", "otype": "company",
            "tags": ["repro:clinics"], "species": ["human"],
            "url": LIST, "desc": " ".join(bits), "checked": "",
        })
        if len(out) % 60 == 0:
            time.sleep(0.6)

    print("  %d records: %d at an address, %d at a state centre"
          % (len(out), exact_n, len(out) - exact_n))
    if dry:
        print("dry run \u2014 nothing written")
        return
    CACHE.write_text(json.dumps(cache, indent=0), encoding="utf-8")
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("Clinics registered under India's ART (Regulation) Act 2021, "
                 "from the National ART and Surrogacy Registry."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


if __name__ == "__main__":
    main()
