# -*- coding: utf-8 -*-
"""What each organisation actually works on.

The entries have facet tags describing what a company IS - a seed major, a
contract laboratory, a trade body. Nothing in them says what organism it works
on, which is the first thing most readers want to filter by.

This file adds that, by hand, keyed on entry name. It is deliberately separate
from ind1.py-ind23.py so it can be filled in batches without touching 23 modules
and re-running the risk of a bad splice through them.

RULES FOLLOWED HERE

An entry lists every organism group it genuinely works on, not the one it is
best known for. Bayer is maize AND soy AND cotton AND canola AND vegetables;
filing it under maize alone is the exact failure that made a text-scraped
version unusable.

An entry with no clear organism gets an empty list rather than a guess. A
patent office, an index fund and a lobbying register do not work on an organism,
and inventing one for them would put noise in every filter.

GROUPS match the release-side classifier in index.html, so a reader moving
between the two layers meets the same words:

    food_crops  vegetables  fibre  forage  trees
    livestock   fish        lab_animals
    insects     microbes    viruses
    human       none
"""

SPECIES = {
    # ---- ind1: the majors, platforms and suppliers -------------------------
    "Bayer Crop Science": ["food_crops", "fibre", "vegetables", "forage"],
    "Corteva Agriscience": ["food_crops", "fibre", "vegetables"],
    "Bayer \u2014 investor filings": [],
    "Corteva \u2014 CRISPR licensing framework": ["food_crops"],
    "Ginkgo Bioworks": ["microbes"],
    "Inari Agriculture": ["food_crops"],
    "Twist Bioscience": ["microbes", "viruses"],
    "Integrated DNA Technologies (Danaher)": ["microbes"],
    "Illumina": [],
    "Addgene": ["microbes", "viruses"],
    "Charles River Laboratories": ["lab_animals", "fish"],
    "Labcorp Drug Development (formerly Covance)": ["lab_animals", "human"],
    "Syngenta Group": ["food_crops", "fibre", "vegetables"],
    "Syngenta \u2014 seedcare & seeds portfolio": ["food_crops", "fibre"],
    "BASF Agricultural Solutions": ["food_crops", "fibre", "microbes"],
    "Rijk Zwaan": ["vegetables"],
    "Limagrain / Vilmorin": ["food_crops", "vegetables"],
    "Oxford Nanopore Technologies": [],
    "BGI Group": ["human"],

    # ---- ind2: animals, wild release, clinical, registers -------------------
    "The Jackson Laboratory": ["lab_animals"],
    "Taconic Biosciences": ["lab_animals"],
    "Envigo / Inotiv": ["lab_animals"],
    "Acceligen (Recombinetics)": ["livestock"],
    "AquaBounty Technologies": ["fish"],
    "ViaGen Pets & Equine": ["livestock", "lab_animals"],
    "Target Malaria": ["insects"],
    "Pivot Bio": ["microbes", "food_crops"],
    "Colossal Biosciences": ["livestock", "lab_animals"],
    "Living Carbon": ["trees"],
    "Vertex / CRISPR Therapeutics \u2014 Casgevy": ["human"],
    "ClinicalTrials.gov": ["human"],
    "Orchid Health": ["human"],
    "CDC ART clinic data": ["human"],
    "Gates Foundation \u2014 committed grants database": [],
    "DARPA \u2014 Biological Technologies Office": ["insects", "microbes", "food_crops"],
    "BIO \u2014 Biotechnology Innovation Organization": [],
    "ISAAA \u2014 GM approval database": ["food_crops", "fibre"],
    "CLEA Japan / Japan SLC": ["lab_animals"],
    "Sooam Biotech": ["lab_animals", "livestock"],
    "Oxitec": ["insects"],
    "HFEA \u2014 licensed clinic register": ["human"],
    "Suzano / FuturaGene": ["trees"],
    "Novartis \u2014 gene therapy": ["human"],
    "IVIRMA Global": ["human"],
    "CropLife International": ["food_crops", "fibre"],
    "OECD BioTrack": ["food_crops", "fibre", "vegetables"],
}

LABELS = {
    "food_crops":  "Food crops",
    "vegetables":  "Vegetables & fruit",
    "fibre":       "Fibre & industrial crops",
    "forage":      "Forage, grass & feed",
    "trees":       "Trees & forestry",
    "livestock":   "Livestock & poultry",
    "fish":        "Fish & aquaculture",
    "lab_animals": "Laboratory animals",
    "insects":     "Insects & gene drives",
    "microbes":    "Microbes & fermentation",
    "viruses":     "Viruses & vectors",
    "human":       "Human & clinical",
}


def species_for(name):
    """Groups this organisation works on. None means not yet assigned; an empty
    list means assigned and genuinely works on no organism."""
    return SPECIES.get(name)


if __name__ == "__main__":
    from collections import Counter
    assigned = len(SPECIES)
    blank = sum(1 for v in SPECIES.values() if not v)
    c = Counter(g for v in SPECIES.values() for g in v)
    bad = sorted({g for v in SPECIES.values() for g in v} - set(LABELS))
    print("entries assigned: %d (%d work on no organism)" % (assigned, blank))
    if bad:
        raise SystemExit("unknown group(s): %s" % ", ".join(bad))
    for g, n in c.most_common():
        print("   %-22s %d" % (LABELS[g], n))
