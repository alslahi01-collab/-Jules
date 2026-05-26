## 2026-05-26 - [Optimized Excel Comparison Logic]
**Learning:** The O(N*M) nested row comparison loop with expensive `fuzz.ratio` and `row.to_dict()` calls is the primary bottleneck. Pre-calculating normalized values, using dictionary lookups for exact matches, and caching fuzzy results significantly reduces execution time.
**Action:** Use dictionary-based grouping for unique normalized values and cache symmetric fuzzy similarity results. Pre-convert DataFrames to records outside the inner loop.
