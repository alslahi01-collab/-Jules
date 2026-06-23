## 2025-05-15 - Initial Profiling
**Learning:** The Excel comparison logic uses a nested $O(N \times M)$ loop with redundant `normalize_arabic` and `fuzz.ratio` calls. `df.iterrows()` and repeated `pd.read_excel` calls add significant overhead.
**Action:** Use `lru_cache` for normalization, pre-calculate normalized values, and use a result cache for fuzzy matching to avoid redundant computations for duplicate or repeated string pairs.
