## 2026-06-26 - Optimized Excel Matching via Unique Value Grouping and Symmetric Caching
**Learning:** Row-by-row fuzzy matching with `iterrows()` and `fuzz.ratio` in an $O(N \times M)$ loop is a major bottleneck. Pre-converting DataFrames to records, grouping by unique normalized values, and using a symmetric results cache for fuzzy scores reduces complexity to $O(U_1 \times U_2)$, where $U$ is the number of unique values.
**Action:** Always group by unique values before fuzzy matching and cache results for unique value pairs. Use `to_dict('records')` for faster row access than `iterrows()`.
