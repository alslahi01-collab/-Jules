## 2025-05-22 - [Optimizing Row Comparison and Sheet I/O]

**Learning:** The application's core bottleneck is an O(N*M) row comparison loop using `iterrows()` and redundant `fuzz.ratio` calls. Additionally, `streamlit_app.py` suffered from O(S1*S2) Excel I/O because the second file was re-read inside the nested sheet loop.

**Action:**
1. Group row indices by unique normalized values to reduce fuzzy matching complexity to O(U1*U2).
2. Use `@functools.lru_cache` for normalization and a results cache for similarity scores.
3. Pre-read and pre-process all sheets of the target Excel file into memory once to avoid redundant I/O.
4. Pre-convert DataFrames to lists of records (`to_dict('records')`) to eliminate `iterrows()` overhead.
