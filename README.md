# Algorithms site — Merge Sort v16

Only the Complexity section of `sorting-merge.html` was changed.

Changes:
- T(n) and the recurrence were removed completely;
- log₂ n is introduced directly as the number of merge levels;
- n = 8 is shown as three merge levels: 1 → 2 → 4 → 8;
- repeated halving gives k = log₂ n;
- a separate block explains why every merge level costs Θ(n);
- the conclusion is Θ(log n) levels × Θ(n) work per level = Θ(n log n).

Everything before Complexity in `sorting-merge.html` is byte-for-byte unchanged.
New styling for the Complexity illustration is appended to `styles.css`.
