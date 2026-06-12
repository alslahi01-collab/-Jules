## 2025-05-15 - [Arabic Text Matching Optimization]
**Learning:** O(N*M) row comparisons in Excel matching are a massive bottleneck. Pre-converting DataFrames to list of records and using a dictionary for exact match lookups reduces complexity to O(N+M) for identical rows. Grouping indices by unique normalized values and caching fuzzy results between those values further reduces expensive `fuzz.ratio` calls from O(N*M) to O(U1*U2).
**Action:** Always pre-convert DataFrames to list of records before high-frequency iteration and use value-based grouping/caching for row comparisons.
