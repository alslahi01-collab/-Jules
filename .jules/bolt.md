## 2025-05-14 - Optimized Excel Fuzzy Matching

**Learning:** The original implementation had O(N*M) complexity for row comparisons, with expensive string normalization and fuzz.ratio calls inside the inner loop. 500x500 rows took ~38 seconds.

**Action:**
1. Added @lru_cache to normalize_arabic.
2. Grouped rows by unique normalized values in a dictionary (norm2_map) to achieve O(1) exact matches.
3. Iterated over unique values for fuzzy matching and cached results for unique string pairs.
4. Pre-processed Excel sheets in the Streamlit app to avoid redundant I/O in nested loops.

**Result:** Reduced 500x500 row comparison time from ~38s to ~1.1s (approx. 34x speedup) with identical results.
