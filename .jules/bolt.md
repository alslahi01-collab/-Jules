## 2025-05-15 - Row comparison bottleneck in Excel matching
**Learning:** The O(N^2) nested loop for row comparison using `iterrows()` and repeated `fuzz.ratio` calls is the primary bottleneck. For 100x100 rows, it takes ~1 second, meaning 1000x1000 would take ~100 seconds.
**Action:** Use dictionary-based lookups for exact matches and cache fuzzy results between unique normalized strings. Avoid `iterrows()` by converting DataFrames to lists of dictionaries. Use `lru_cache` for string normalization.
