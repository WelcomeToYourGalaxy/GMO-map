# -*- coding: utf-8 -*-
"""Industry entries, part 63. The boundary, and the four ways it leaks.

Guide 4 says the question that undoes declarations is what happens at the
boundary, and that it is answerable in advance. These are the answers.

They are unglamorous and they are what actually decides whether a GM-free
region holds. A declaration fails at one of four points, and only the first is
the one people expect:

  pollen crossing the line          the expected route, and the most studied
  a shared combine                  the commonest, and nobody legislates it
  a lorry or a storage bin          invisible, and it happens off the farm
  the seed lot itself               already mixed before anything was planted

Notification registries are here too, because the whole set depends on knowing
what a neighbour intends before they do it rather than after.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND63 = {}

# ============================================== KNOWING IN ADVANCE ===========
IND63["USA"] = [
 e("DriftWatch \u2014 mapping sensitive sites before spraying",
   "https://driftwatch.org/",
   "A public register where beekeepers, organic growers and others map their sites "
   "so applicators can see them before spraying. Used across many US states, free "
   "to register, and checked by commercial applicators as a matter of routine. "
   "Registering costs an afternoon and does two things at once: it may prevent the "
   "drift, and if drift happens anyway it establishes that the applicator could "
   "have known. That second effect is what makes it worth doing even where nobody "
   "checks it.",
   ["rules:standards", "seed:distribution"], base=ASSN),
]

# ============================================== THE SHARED MACHINE ===========
# ================================================ THE SEED ITSELF ============
