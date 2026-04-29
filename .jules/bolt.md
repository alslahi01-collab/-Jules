## 2025-05-14 - [Performance Improvement: Excel Row Comparison]
**Learning:** Nested row-by-row fuzzy matching (O(N*M)) is extremely slow. In this codebase, many rows share identical or similar values. By grouping rows by unique normalized values and caching similarity scores between unique pairs, complexity is reduced from O(N*M) to O(U1*U2) where U are unique values. Additionally, using a symmetric cache key for similarity scores halves the remaining computations.

**Action:** Always prefer dictionary-based grouping and unique value comparison over direct row-by-row iteration for N^2 comparison tasks. Implement lru_cache for expensive normalization functions.
