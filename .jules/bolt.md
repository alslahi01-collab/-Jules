## 2025-05-22 - [Optimized Row Comparison Logic]
**Learning:** Nested loops over DataFrame rows with `iterrows()` and `fuzz.ratio` are extremely slow (O(N*M)). Using `df.to_dict('records')` and grouping indices by unique normalized values reduces complexity to O(U1*U2) where U is the number of unique values. Caching normalization also provides a small boost.
**Action:** Always prefer grouping by unique values and record-based iteration for fuzzy matching tasks between two datasets.
