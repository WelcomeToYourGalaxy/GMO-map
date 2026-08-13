# -*- coding: utf-8 -*-
"""Which approach each country takes to deciding what counts as a regulated
organism.

Three approaches, and the difference decides everything downstream:

    technique   regulated because of HOW it was made. A gene-edited plant
                generally stays inside the scheme, so it produces an
                application, an assessment and a register entry.
    trait       regulated because of WHAT it is. The method does not matter,
                which in practice waves most gene-edited organisms through.
    carveout    at least one class of engineered organism has been placed
                outside registration entirely - usually organisms edited
                without inserting DNA from another species.

WHERE THIS COMES FROM, AND WHAT IT IS NOT

There is no register of this. No treaty body publishes a table of which country
uses which approach, because the classification is a judgement about a statute
rather than a field anyone fills in. The Cartagena Protocol's Biosafety
Clearing-House holds national reports from its parties, the FAO GM Foods Platform
holds approvals, and neither answers this question directly.

So this is a reading of national frameworks, compiled from the BCH country
profiles, national biosafety statutes, and the published comparative literature.
It will be wrong in places and it will go out of date: several countries are
mid-reform, and the EU's new genomic techniques proposal would move the whole
bloc from technique-based to a carve-out if it passes.

CONFIDENCE is recorded per country rather than hidden:

    firm     the statute is explicit and has been applied
    likely   the framework is clear but the edited-organism position is
             inferred from practice rather than stated in law
    thin     a law exists and its treatment of editing is genuinely unsettled
             or not retrievable

A country listed here is never "a country without rules". Almost every state has
a biosafety law of some kind. This says which of three shapes it takes.
"""

# ---------------------------------------------------------------------------
# TECHNIQUE-BASED: the method triggers regulation.
# ---------------------------------------------------------------------------
TECHNIQUE = {
    # Europe outside the EU, and EU members pending the NGT reform
    "NZL": "firm", "NOR": "firm", "CHE": "firm", "ISL": "likely",
    "AUT": "firm", "HUN": "firm", "SRB": "firm", "BIH": "protocol",
    "MKD": "protocol", "ALB": "protocol", "MNE": "protocol", "MDA": "likely",
    "TUR": "firm", "UKR": "likely", "BLR": "likely", "RUS": "firm",
    # EU member states: the directive is technique-based following the 2018
    # Court of Justice ruling. Listed individually because the NGT proposal
    # would move them, and because member states differ on cultivation.
    "DEU": "firm", "FRA": "firm", "ITA": "firm", "ESP": "firm",
    "NLD": "firm", "BEL": "firm", "PRT": "firm", "IRL": "firm",
    "POL": "firm", "CZE": "firm", "SVK": "firm", "SVN": "firm",
    "HRV": "firm", "ROU": "firm", "BGR": "firm", "GRC": "firm",
    "SWE": "firm", "DNK": "firm", "FIN": "firm", "EST": "firm",
    "LVA": "firm", "LTU": "firm", "CYP": "firm", "LUX": "firm",
    "MLT": "firm",
    # Asia and the Middle East
    "IND": "firm", "IRN": "likely", "IRQ": "thin", "SYR": "thin",
    "LBN": "thin", "JOR": "likely", "SAU": "likely", "KWT": "thin",
    "QAT": "thin", "OMN": "thin", "YEM": "thin", "AZE": "protocol",
    "ARM": "protocol", "GEO": "likely", "KAZ": "likely", "UZB": "protocol",
    "TKM": "protocol", "TJK": "protocol", "KGZ": "protocol", "MNG": "protocol",
    "LKA": "likely", "NPL": "protocol", "BTN": "protocol", "MDV": "protocol",
    "KHM": "protocol", "LAO": "protocol", "MMR": "protocol",
    # Africa and the Americas
    "EGY": "firm", "TUN": "likely", "DZA": "likely", "MAR": "likely",
    "LBY": "thin", "SDN": "protocol", "MEX": "firm", "PER": "firm",
    "ECU": "firm", "BOL": "firm", "VEN": "firm", "CRI": "likely",
    "PAN": "protocol", "NIC": "protocol", "SLV": "protocol", "GTM": "likely",
    "HND": "protocol", "CUB": "likely", "DOM": "protocol", "JAM": "protocol",
    "TTO": "protocol", "HTI": "protocol",
    # ---- added from the Cartagena party list ------------------------------
    # Every state below is a Party to the Cartagena Protocol on the
    # Secretariat's own ratification list, and none has an editing exemption
    # this map has been able to find. The Protocol defines a living modified
    # organism by the technique used to make it, so a country that enacted
    # that definition and has not since carved editing out is technique-based
    # by construction. That is what 'protocol' records: read from the treaty
    # rather than from a national statute, and marked so nobody mistakes it
    # for a reading of the law on the ground.
    #
    # Six are marked 'thin' instead. In each, the question is not which shape
    # the statute takes but whether any of it is being administered.
    # Africa
    "AGO": "protocol", "BDI": "protocol", "BEN": "protocol", "CAF": "thin",
    "COD": "protocol", "COG": "protocol", "COM": "protocol", "CPV": "protocol",
    "DJI": "protocol", "ERI": "thin", "GAB": "protocol", "GIN": "protocol",
    "GMB": "protocol", "GNB": "protocol", "LBR": "protocol", "LSO": "protocol",
    "MDG": "protocol", "MRT": "protocol", "MUS": "protocol", "SOM": "thin",
    "SYC": "protocol", "TCD": "protocol", "TGO": "protocol",
    # The Caribbean and the Americas
    "ATG": "protocol", "BHS": "protocol", "BLZ": "protocol", "BRB": "protocol",
    "DMA": "protocol", "GRD": "protocol", "GUY": "protocol", "KNA": "protocol",
    "LCA": "protocol", "SUR": "protocol", "VCT": "protocol",
    # The Pacific
    "FJI": "protocol", "KIR": "protocol", "MHL": "protocol", "NRU": "protocol",
    "PLW": "protocol", "PNG": "protocol", "SLB": "protocol", "TON": "protocol",
    "WSM": "protocol",
    # Asia and the Middle East
    "AFG": "thin", "ARE": "protocol", "BHR": "protocol", "PRK": "thin",
    "PSE": "thin",
}

# ---------------------------------------------------------------------------
# TRAIT-BASED: what the organism IS triggers regulation, not the method.
# ---------------------------------------------------------------------------
TRAIT = {
    "CAN": "firm",   # the clearest case anywhere: novel traits, any method
    "USA": "firm",   # product-based across USDA, FDA and EPA
}

# ---------------------------------------------------------------------------
# CARVE-OUT: a class of engineered organism sits outside registration.
# ---------------------------------------------------------------------------
CARVEOUT = {
    # The Americas, where the carve-out approach was established
    "ARG": "firm", "BRA": "firm", "CHL": "firm", "PRY": "firm",
    "URY": "firm", "COL": "firm",
    # Asia-Pacific
    "AUS": "firm", "JPN": "firm", "PHL": "firm", "THA": "likely",
    "VNM": "likely", "IDN": "likely", "MYS": "likely", "SGP": "likely",
    "KOR": "firm", "CHN": "firm", "TWN": "likely", "BGD": "likely",
    "PAK": "likely", "ISR": "firm",
    # Africa
    "NGA": "firm", "KEN": "firm", "GHA": "firm", "ZAF": "firm",
    "ETH": "likely", "UGA": "likely", "TZA": "protocol", "ZMB": "protocol",
    "MWI": "likely", "MOZ": "likely", "ZWE": "protocol", "RWA": "likely",
    "SEN": "likely", "BFA": "firm", "MLI": "protocol", "NER": "protocol",
    "CIV": "likely", "CMR": "protocol", "SWZ": "likely", "NAM": "protocol",
    "BWA": "protocol",
    # and the UK, which diverged from the EU with the Precision Breeding Act
    "GBR": "firm",
}

CONF_NOTE = {
    "firm":   "The statute is explicit on this and has been applied.",
    "likely": ("The framework is clear; the position on gene-edited organisms is "
               "inferred from how it has been applied rather than stated in law."),
    "protocol": ("Classified from the law itself rather than from practice. This "
                 "country implements the Cartagena Protocol, and the Protocol "
                 "defines a living modified organism by the technique used to make "
                 "it. A country that enacted that definition and has not since "
                 "written an editing exemption is technique-based by construction, "
                 "whether or not it has ever had an edited organism to assess."),
    "thin":   ("A biosafety law is on the books and this map cannot verify what it "
               "currently means. Several of these states are in or recovering from "
               "armed conflict, where the question is not which approach the "
               "statute takes but whether any of it is being administered. Shown "
               "rather than left blank, because a gap on a map reads as a country "
               "without rules, and marked so the shading is not mistaken for a "
               "finding."),
}


def classified():
    """iso3 -> (regime, confidence). One dict, checked for collisions."""
    out, seen = {}, {}
    for regime, table in (("technique", TECHNIQUE), ("trait", TRAIT),
                          ("carveout", CARVEOUT)):
        for iso, conf in table.items():
            if iso in seen:
                raise ValueError("%s classified twice: %s and %s"
                                 % (iso, seen[iso], regime))
            seen[iso] = regime
            out[iso] = (regime, conf)
    return out


if __name__ == "__main__":
    c = classified()
    from collections import Counter
    print("countries classified: %d" % len(c))
    print("by regime:   %s" % dict(Counter(v[0] for v in c.values())))
    print("by evidence: %s" % dict(Counter(v[1] for v in c.values())))
