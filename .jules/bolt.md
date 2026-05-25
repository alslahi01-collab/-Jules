## 2026-05-25 - Optimized Row Comparison Performance
**Learning:** In Excel comparison tasks, performing O(N*M) row-by-row comparisons using `df.iterrows()` and repeated string normalization/fuzzy matching is a major bottleneck. Pre-converting DataFrames to records (`to_dict('records')`), grouping indices by unique normalized values in a dictionary, and caching `fuzz.ratio` results for unique value pairs achieved a ~21x speedup (53.2s down to 2.5s for 500x500 rows).

**Action:** Always avoid `iterrows()` for large datasets. Use dictionary-based grouping for O(1) exact matches and pair-based result caching for fuzzy matches to reduce complexity from O(N*M) to O(U1*U2) where U is the number of unique values.
