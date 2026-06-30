## 2025-05-14 - [Excel Matching Complexity Reduction]
**Learning:** Nested row-by-row comparison with `df.iterrows()` and fuzzy matching has $O(N \times M)$ complexity. Grouping rows by unique normalized values and caching fuzzy results for string pairs reduces complexity to $O(U_1 \times U_2)$, where $U$ is the number of unique values. Using `df.to_dict('records')` is also significantly faster than `iterrows()`.
**Action:** Always prefer unique-value grouping and record-based iteration for large dataset comparisons involving expensive similarity functions.
