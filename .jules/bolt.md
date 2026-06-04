## 2025-05-21 - Fuzzy Matching Complexity Bottleneck
**Learning:** The O(N*M) nested loop in Excel comparison is the primary bottleneck. Iterating with `df.iterrows()` and repeatedly calling normalization and `fuzz.ratio` on the same strings leads to massive redundancy.
**Action:**
1. Use `df.to_dict('records')` to speed up row iteration.
2. Group unique normalized values into a dictionary (`norm_map`) to handle exact matches in O(1) and reduce fuzzy matching to O(U1*U2).
3. Use a symmetric results cache for `fuzz.ratio` to avoid redundant O(N^2) similarity calculations.
4. Apply `@functools.lru_cache` to normalization functions to avoid repeated regex operations.
