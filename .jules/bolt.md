## 2025-05-14 - [Excel Matching Optimization]
**Learning:** Nested loops in row-by-row Excel comparison are extremely slow (O(N*M)). Using `df.iterrows()` adds significant overhead. Grouping by unique normalized values and caching fuzzy match results between those unique values reduces the complexity to O(U1*U2) where U is the number of unique values.
**Action:** Always pre-convert DataFrames to list of records (`to_dict('records')`) for faster iteration, and use dictionaries to group indices by normalized values to avoid redundant O(N²) fuzzy matching.
