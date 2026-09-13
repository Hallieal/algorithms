AHA — Sorting fixes v4
======================

This update keeps the latest Practice Problems files and adds a small source patch
for the existing full website.

What it fixes
-------------
1. Replaces the accidental mathematical placeholder Θ(loglinear) with Θ(n log n)
   in:
   - sorting-merge.html
   - sorting-quick.html
   - sorting-merge-ru.html
   - sorting-quick-ru.html

   The ordinary word "loglinear" in prose/headings is intentionally left unchanged.

2. Adds unobtrusive Practice links to sorting-applications.html:
   - Pairs and intervals -> Two Sum in a Sorted Array; Meeting Rooms
   - Combining ordered data -> Merge Without Extra Space
   - Order-based summaries -> K Smallest Elements

3. Practice Problems remains English-only for now. No fake RU language switch is
   added before a complete Russian translation exists.

How to apply
------------
Extract this archive into the root of the algorithms repository, preserving the
existing files. Then run one of:

    python apply_site_fixes.py

or on Windows double-click:

    APPLY_FIXES.bat

The script is idempotent: running it again will not duplicate the new links.
Afterwards run:

    git diff

and commit/push the changed files as usual.
