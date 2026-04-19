## 2025-05-23 - Hash-map based row matching and caching

**Learning:** The previous implementation of Excel row comparison had O(N*M) complexity with expensive `fuzz.ratio` calls inside the nested loop. Additionally, repeated `pd.read_excel` calls for the same sheet metadata caused excessive I/O.

**Action:**
1. Use hash-maps (dictionaries) to group rows by their normalized values. This enables O(1) exact matching and allows performing fuzzy matching only once per unique value pair.
2. Implement caching for normalization and fuzzy matching using `functools.lru_cache`.
3. Pre-load sheet metadata or entire sheets into memory before entering comparison loops to minimize redundant I/O.
4. Measured ~12x speedup for 500x500 rows.
