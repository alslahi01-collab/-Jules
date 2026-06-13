## 2026-06-13 - [Fuzzy matching O(N*M) complexity]
**Learning:** In row comparison loops, using `df.iterrows()` and performing fuzzy matching between every row pair is extremely slow for large datasets. Pre-converting to records and grouping indices by unique normalized values allows reducing the comparison to O(U1*U2), where U is the number of unique values. Caching fuzzy matching results between unique value pairs further eliminates redundant computations.
**Action:** Always group by unique values and use a results cache for expensive similarity functions like `fuzz.ratio`.
