AHA Sorting update v5

IMPORTANT
---------
The previous v4 archive did not contain sorting-applications.html or the long
Merge/Quick lecture files. That is why simply unpacking it produced no visible
change. v5 fixes that mistake for Applications directly.

DIRECT REPLACEMENT INCLUDED
---------------------------
- sorting-applications.html
  Adds compact Practice links to:
  * Two Sum in a Sorted Array
  * Meeting Rooms
  * Merge Without Extra Space
  * K Smallest Elements

The current Practice Problems files from the previous update are also included.

MERGE / QUICK TYPO FIX
----------------------
The four long lecture files themselves are not bundled here because they were
not available as local editable files in this session. Run the included patch
from the ROOT OF YOUR REPOSITORY (where sorting-merge.html lives):

    python apply_formula_fixes.py

On Windows you can double-click APPLY_FORMULA_FIXES.bat.

It replaces every exact occurrence of:
    Θ(loglinear)
with:
    Θ(n log n)
in:
    sorting-merge.html
    sorting-quick.html
    sorting-merge-ru.html
    sorting-quick-ru.html

The script prints how many replacements it made and fails loudly if any target
file is missing.
