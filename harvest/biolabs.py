#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Maximum-containment laboratories, from Global BioLabs.

There is no international register of BSL4 laboratories and no obligation to
declare one. The Biological Weapons Convention asks states to describe their
maximum-containment facilities in an annual return, and between 2017 and 2021
fewer than half of the 185 states parties submitted anything; of the twenty
countries with an operating BSL4 lab, nine publish theirs. So a research project
at King's College London and the Schar School is the only global account there
is, and its gaps are the gaps in what can be found out rather than in what
exists.

WHERE THE DATA COMES FROM, AND WHY IT ARRIVES BY HAND.

The published report gives regional totals and country scores and names no
laboratory. The interactive map draws from a Mapbox vector tileset, which is not
a file and cannot be fetched: the points exist only once a browser has rendered
them. The dataset is therefore exported from the map itself, in the browser, and
dropped into harvest/biolabs/ as JSON. See the README there for the command.

That also means an export only contains what was on screen when it ran. This
harvester merges every file it finds and deduplicates, so several partial
exports covering different parts of the world add up to a whole, and it says how
far short of the published totals it is rather than implying the file is
complete.

    python3 harvest/biolabs.py
    python3 harvest/biolabs.py --dry-run
"""

import json, re, sys, time, pathlib

HERE = pathlib.Path(__file__).resolve().parent
INDIR = HERE / "biolabs"
OUT = HERE / "biolabs.json"

SRC = "https://www.globalbiolabs.org/"

# The report's own counts, so a partial export can say so.
PUBLISHED = {"bsl4": 69, "bsl3plus": 57}

LAYER_LABEL = {
    "bsl4":     "BSL4 laboratory",
    "rbsl4":    "BSL4 laboratory",
    "absl4":    "BSL4 animal laboratory",
    "bsl3plus": "BSL3+ laboratory",
}


def _s(rec, *keys):
    """Fields differ in capitalisation between layers - 'Research focus' in one
    and 'Research Focus' in another - so every spelling is asked for."""
    for k in keys:
        v = rec.get(k)
        if v not in (None, "", "N/A"):
            return str(v).strip()
    for k in keys:
        want = k.lower()
        for kk, v in rec.items():
            if str(kk).lower().lstrip("\ufeff") == want and v not in (None, "", "N/A"):
                return str(v).strip()
    return ""


def load():
    files = sorted(INDIR.glob("*.json")) if INDIR.exists() else []
    rows = []
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print("  ! %s unreadable (%s)" % (f.name, e), file=sys.stderr)
            continue
        if isinstance(d, dict):
            d = d.get("features") or d.get("rows") or []
        rows += [r for r in d if isinstance(r, dict)]
        print("  %-28s %d records" % (f.name[:28], len(d)))
    return rows


def main():
    dry = "--dry-run" in sys.argv
    rows = load()
    if not rows:
        print("No exports in %s.\n"
              "  Open https://global-biolabs.github.io/ and run the command in\n"
              "  %s/README.md, then drop the file here. Nothing written."
              % (INDIR, INDIR), file=sys.stderr)
        return

    # Deduplicate on name and position: a lab appears once per layer it belongs
    # to, and the same lab turns up again in an overlapping export.
    seen, merged = {}, []
    for r in rows:
        nm = _s(r, "Name")
        if not nm:
            continue
        try:
            lat = float(_s(r, "Latitude") or r.get("lat"))
            lng = float(_s(r, "Longitude") or r.get("lng"))
        except (TypeError, ValueError):
            continue
        key = (nm.lower(), round(lat, 3), round(lng, 3))
        if key in seen:
            # keep the richer record, and remember every layer it appeared in
            seen[key]["_layers"].add(r.get("layer") or "")
            if len(json.dumps(r)) > len(json.dumps(seen[key]["_r"])):
                seen[key]["_r"] = r
            continue
        seen[key] = {"_r": r, "_layers": {r.get("layer") or ""},
                     "lat": lat, "lng": lng, "name": nm}
        merged.append(seen[key])

    out = []
    counts = {"bsl4": 0, "bsl3plus": 0}
    for m in merged:
        r, lay = m["_r"], m["_layers"]
        is3 = "bsl3plus" in lay
        counts["bsl3plus" if is3 else "bsl4"] += 1
        kind = ("BSL3+ laboratory" if is3 else
                "BSL4 animal laboratory" if "absl4" in lay else "BSL4 laboratory")
        status = _s(r, "Status") or "status not stated"
        typ = _s(r, "Type of Lab").title()
        focus = _s(r, "Research focus", "Research Focus")
        size = _s(r, "Size of BSL 4 space (square meters)")
        aff = _s(r, "Institutional Affiliation")
        addr = _s(r, "Address")
        cont = _s(r, "Containment Type (Glove Box, Suit, or Both)")
        urban = _s(r, "Urban?")
        opened = _s(r, "Date lab was operational, expected or announced")

        # "A bsl4 animal laboratory" read as a typo. The level is an initialism
        # and keeps its capitals; only the rest of the phrase is lowered.
        _k = kind.replace("BSL4", "BSL4").replace("BSL3+", "BSL3+")
        bits = ["A %s%s." % (_k[0].upper() + _k[1:],
                             (", " + status.lower()) if status else "")]
        if aff:
            bits.append("Run by %s." % aff)
        if typ:
            _f = {"both": "both human and animal health",
                  "human": "human health", "animal": "animal health"}.get(
                      focus.lower(), (focus.lower() + " health") if focus else "")
            bits.append("It is categorised as a %s laboratory%s." %
                        (typ.lower(), (", working on " + _f) if _f else ""))
        # "Personnel work in unknown" was worse than saying nothing.
        if cont and cont.lower() not in ("unknown", "n/a", "not stated"):
            bits.append("Personnel work in %s." %
                        {"Suit": "full-body positive-pressure suits with their own "
                                 "air supply",
                         "Glove Box": "sealed cabinets, handling material through "
                                      "glove ports",
                         "Both": "both pressure suits and sealed cabinets"}
                        .get(cont, cont.lower()))
        if size:
            bits.append("Containment space: %s." % size)
        if opened:
            bits.append("Operational or announced: %s." % opened)
        if urban.lower().startswith("y"):
            bits.append("It stands in a built-up area, with more than fifty "
                        "thousand people living within two and a half miles.")
        bits.append("There is no international register of laboratories at this "
                    "containment level and no obligation to declare one, so this "
                    "record comes from a research project rather than a "
                    "regulator. What that project could not find out is absent "
                    "here too.")

        out.append({
            "name": m["name"][:150],
            "source": "industry:animals",
            "type": kind,
            "lat": round(m["lat"], 5), "lng": round(m["lng"], 5),
            "state": ", ".join(x for x in (addr[:70], _s(r, "Country")) if x),
            # The dataset carries a street address and a coordinate pair from
            # the project's own geocoding, so these are operational positions.
            "precise": True,
            "addr_grade": "operational" if addr else "centroid",
            "impact": 4 if not is3 else 3,
            "company": aff, "size": size,
            "status": status,
            "phase": "post", "date": opened, "otype": "institute",
            "tags": ["animals:services"], "species": ["microbes"],
            "url": _s(r, "Website") or SRC,
            "desc": " ".join(bits), "checked": "",
        })

    print("  %d laboratories: %d BSL4, %d BSL3+"
          % (len(out), counts["bsl4"], counts["bsl3plus"]))
    for k, pub in PUBLISHED.items():
        got = counts[k]
        if got < pub:
            print("     %s: %d of the %d the 2023 report counts \u2014 an export "
                  "only holds what was on screen when it ran" % (k, got, pub))
    if dry:
        print("dry run \u2014 nothing written")
        return
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("BSL4 and BSL3+ laboratories from Global BioLabs, a research "
                 "project at King's College London and the Schar School. There "
                 "is no official register of these facilities anywhere."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


if __name__ == "__main__":
    main()
