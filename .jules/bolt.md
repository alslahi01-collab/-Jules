## 2025-05-21 - [Excel Comparison Bottlenecks]
**Learning:** The O(N*M) row comparison with `df.iterrows()` and repeated `fuzz.ratio` calls is the primary bottleneck. Pre-converting to records and grouping by unique normalized values provides a ~60x speedup. In `streamlit_app.py`, re-reading all sheets of the target file within the outer sheet loop adds significant I/O overhead.
**Action:** Use `lru_cache` for normalization, group indices by unique values for matching, and cache fuzzy results between unique value pairs. In multi-sheet scenarios, pre-read target sheets into memory once.
