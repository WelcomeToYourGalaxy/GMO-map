# APHIS exports go here

## Start with the workbook, not the search tool

    https://www.aphis.usda.gov/animal-welfare/list-active-licensees-registrants

"List of active licensees and registrants" is one download holding every active
certificate — 12,443 in the July 2026 edition, including 849 Class R research
facilities, 51 Class F federal, 58 Class V Veterans Affairs and 37 Class G
Agricultural Research Service. Drop the .xlsx straight in this folder.

It carries a mailing city and a state and no street address, so on its own it
gives complete coverage at low precision.

## Then the search tool, for street addresses

    https://aphis.my.site.com/PublicSearchTool/s/

Export caps at 100 rows, and the site reports 31,862 licensees and 18,935
registrants — but those totals count every certificate ever issued, most of them
long cancelled. The active ones are the 12,443 already in the workbook. So use
the search tool only to add street addresses, filtered to Registration Type
`Class R - Research Facility` AND Certificate Status `Active`, and work through
in batches.

Any number of files, either format, any order. `aphis_animal_facilities.py`
merges by certificate number field by field, so a row with a street address beats
one without no matter which file it came from, and the workbook's Active status
overrides a stale "Cancelled" from an older export.

## Classes

Research is not only Class R. Federal research facilities file under F, Veterans
Affairs hospitals under V, and the Agricultural Research Service under G — 146
active certificates that a filter on "Class R" misses.
