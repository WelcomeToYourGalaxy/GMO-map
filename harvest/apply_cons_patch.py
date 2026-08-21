#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three text-anchored edits to index.html for the consultations panel.

No line numbers: every anchor is asserted to match EXACTLY ONCE, and the script
refuses to write anything if any anchor misses or is ambiguous. A multi-edit
script whose last anchor fails must not leave the file half-edited, so the
edits are applied to a string in memory and the file is written once at the end.

    python3 apply_cons_patch.py index.html
"""
import sys, pathlib

EDITS = []


def edit(name, old, new):
    EDITS.append((name, old, new))


# ---------------------------------------------------------------- edit 1 -----
# The client subject filter is English-only, and the new ePing feed carries
# titles as members filed them. Three of five realistic non-English rows were
# being dropped here AFTER the harvester correctly kept them - a second filter,
# quietly stricter than the first, which is the same class of fault as the
# harvester's own AND-of-two-filters.
edit("PJ_CONS_TERMS: non-English forms",
     """    'synthetic biology', 'gene therapy', 'cell therapy', 'germline',
    'embryo', 'in vitro fertil', 'assisted reproduct', 'clone', 'cloning',
    'plant variety', 'upov', 'seed', 'cultivar', 'pollen', 'landrace'
  ];""",
     """    'synthetic biology', 'gene therapy', 'cell therapy', 'germline',
    'embryo', 'in vitro fertil', 'assisted reproduct', 'clone', 'cloning',
    'plant variety', 'upov', 'seed', 'cultivar', 'pollen', 'landrace',
    /* The WTO feed carries each notification's title as the member filed it,
       and the members this source exists to reach are largely not Anglophone.
       Without these, 'Reglamento sobre organismos vivos modificados' and
       'Cadre de biosecurite' are dropped here after the harvester correctly
       kept them, and the panel is quietly Anglophone while looking global.
       Accented and unaccented spellings both appear in the file. */
    'organismos vivos modificados', 'organismes vivants modifi',
    'organismos geneticamente modificados', 'geneticamente modificad',
    'gen\\u00e9ticamente modificad', 'g\\u00e9n\\u00e9tiquement modifi',
    'modificados geneticamente', 'transgen', 'transg\\u00e9n',
    'transg\\u00eanic', 'bioseguridad', 'biosseguran', 'bioseguran',
    'bios\\u00e9curit', 'biosecurit', 'biotecnolog'
  ];""")

# ---------------------------------------------------------------- edit 2 -----
# 'OGM' and 'OVM' are the standard abbreviations in French/Spanish/Portuguese
# filings. They go in the word-boundary set rather than the substring list for
# the same reason 'gm' and 'ge' do.
edit("PJ_CONS_WORDS: OGM / OVM",
     """  var PJ_CONS_WORDS = /\\b(gm|gmos?|lmos?|genes?|bt|ge)\\b/i;""",
     """  var PJ_CONS_WORDS = /\\b(gm|gmos?|lmos?|genes?|bt|ge|ogm|ovm|vgm)\\b/i;""")

# ---------------------------------------------------------------- edit 3 -----
# The empty state said one thing for two different situations. "No open comment
# window is recorded right now" is a claim about the world; a failed harvest is
# a fact about the pipeline. The harvester now writes sources_reached /
# sources_total, so the panel can tell them apart instead of asserting the
# stronger of the two on no evidence.
edit("empty state distinguishes a failed fetch from an empty world",
     """      if(!g.keys.length){
        host.innerHTML = '<div class="cons-note">No open comment window is '
          + 'recorded right now. This box stays empty rather than showing a '
          + 'window that has since shut \\u2014 a closed consultation presented as '
          + 'open sends somebody to write a comment nobody has to read.</div>';
        return true;
      }""",
     """      if(!g.keys.length){
        /* Two different situations, and they were saying the same sentence.
           "Nothing is open" is a claim about the world. "We could not fetch"
           is a fact about this pipeline, and asserting the first on the
           strength of the second tells a reader in a country with a window
           closing on Friday that there is nothing to do. */
        var reach = PJ_CONS && PJ_CONS.sources_reached,
            tot   = PJ_CONS && PJ_CONS.sources_total;
        host.innerHTML = '<div class="cons-note">'
          + ((reach === 0 || (tot && reach != null && reach < tot))
             ? 'Some sources could not be read on the last harvest'
               + (tot ? ' (' + reach + ' of ' + tot + ' answered)' : '')
               + ', so this list may be short. It is not a statement that '
               + 'nothing is open \\u2014 check the venues under each country '
               + 'below.'
             : 'No open comment window is recorded right now. This box stays '
               + 'empty rather than showing a window that has since shut '
               + '\\u2014 a closed consultation presented as open sends '
               + 'somebody to write a comment nobody has to read.')
          + '</div>';
        return true;
      }""")


def main():
    path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    src = path.read_text(encoding="utf-8")
    out, problems = src, []
    for name, old, new in EDITS:
        n = out.count(old)
        if n != 1:
            problems.append("%-56s %d matches" % (name, n))
            continue
        out = out.replace(old, new)
        print("  ok   %s" % name)
    if problems:
        print("\nNOT WRITTEN - every anchor must match exactly once:",
              file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        sys.exit(1)
    path.write_text(out, encoding="utf-8")
    print("\nwrote %s (%d bytes, was %d)" % (path.name, len(out), len(src)))


if __name__ == "__main__":
    main()
