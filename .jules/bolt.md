## 2026-04-21 - Optimized Row Comparison with Hash Maps and Caching
**Learning:** Nested loops with `iterrows()` and repeated fuzzy matching are the primary bottleneck in Excel comparison tools. Using `to_dict('records')` for faster access and a dictionary-based hash map for exact matches significantly reduces complexity. Caching fuzzy match scores between unique normalized values avoids redundant (N^2)$ computations when values are repeated.
**Action:** Always prefer dictionary lookups for exact matches and cache fuzzy results for unique value pairs in row-by-row comparison scenarios.
