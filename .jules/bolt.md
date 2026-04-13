## 2025-05-14 - Optimized Excel Comparison Engine

**Learning:** The previous implementation used O(N * M) nested loops for row-by-row comparison, calling `normalize_arabic` and `fuzz.ratio` repeatedly even for identical values. Additionally, in `streamlit_app.py`, the second Excel file was being re-read from disk for every sheet in the first file.

**Action:**
1. Applied `functools.lru_cache` to `normalize_arabic`.
2. Pre-calculated normalized values for entire columns using vectorized `apply`.
3. Used dictionary-based lookup (`defaultdict(list)`) to map normalized strings to row indices, allowing O(N) exact matching.
4. Performed fuzzy matching only on unique pairs of normalized strings, reducing complexity to O(U1 * U2).
5. Pre-read and cached DataFrames and metadata for all sheets of the target file in memory once before starting the comparison loop.

**Impact:** Reduced 150x150 comparison time from 3.92s to 0.12s (~97% speedup).
