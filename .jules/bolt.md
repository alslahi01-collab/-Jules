## 2026-04-30 - Optimized Row Comparison with Dictionary Lookups and Caching

**Learning:** In applications performing O(N*M) row comparisons (like fuzzy matching between two datasets), the primary bottleneck is often redundant string processing and expensive similarity calculations (e.g., `fuzz.ratio`). Grouping data by unique normalized values into a hash-map (dictionary) allows performing exact matching in O(N) and significantly reduces the number of fuzzy matching calls from O(N*M) to O(U1*U2) where U is the number of unique values.

**Action:**
1. Use `functools.lru_cache` on normalization functions.
2. Group comparison rows by normalized values in a dictionary.
3. Cache fuzzy similarity results between unique pairs of strings to avoid redundant O(N^2) work when duplicate values exist across rows.
4. Convert DataFrames to dictionaries (`to_dict('records')`) for faster access in tight loops compared to `.iterrows()`.

**Impact:**
- 100x100 row comparison (250k potential operations in original exhaustive logic): Reduced from ~1.44s to ~0.10s (~14x speedup).
