## 2025-05-22 - Optimized Excel Comparison Logic
**Learning:** Found O(N*M) nested loops in `process_sheets` performing redundant string normalization and `fuzz.ratio` calls. Using `df.iterrows()` inside nested loops is a major performance killer.
**Action:**
1. Optimized `normalize_arabic` with `@lru_cache`.
2. Pre-converted DataFrames to lists of records (`df.to_dict('records')`) for faster iteration.
3. Grouped rows by unique normalized values to reduce `fuzz.ratio` complexity from O(N*M) to O(U1*U2).
4. Cached fuzzy results between unique string pairs.
**Result:** ~75x speedup for 100x100 rows (1.9s -> 0.02s).
