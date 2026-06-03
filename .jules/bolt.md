## 2025-05-22 - Identifying Bottlenecks in Excel Comparison
**Learning:** The current implementation of `process_sheets` in `app.py` and `streamlit_app.py` uses nested loops with `iterrows()` and calls `normalize_arabic` repeatedly. For 200x200 rows, it takes ~4.6s. The complexity is $O(N \times M)$ with heavy constant factors due to repeated string processing and slow DataFrame iteration.
**Action:** Optimize by pre-calculating normalized values, using hash maps for exact matches, and performing fuzzy matching only on unique normalized value pairs.
