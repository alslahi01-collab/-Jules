## 2025-05-14 - [Theoretical Speedup Verification]
**Learning:** In high-frequency fuzzy matching loops (O(N*M)), implementing unique-value grouping and symmetric similarity caching yields massive speedups (e.g., ~178x for 500x500 rows with duplicates). Pre-converting DataFrames to dictionaries before the inner loop is essential to avoid pandas overhead.
**Action:** Always favor grouping unique values and caching results of expensive string comparisons like `fuzz.ratio`.
