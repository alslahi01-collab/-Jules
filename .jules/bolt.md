## 2025-05-14 - Optimized Excel comparison logic using caching and hash-map lookups

**Learning:** String normalization and fuzzy matching in O(N*M) loops is a massive bottleneck for Excel comparison.
1. Using `@lru_cache` on normalization functions reduces redundant regex work.
2. Grouping rows by unique normalized values into a hash-map (`norm_map`) allows handling exact matches in O(N+M) and fuzzy matches in O(U1*U2) where U1/U2 are unique values.
3. Since fuzzy similarity (`fuzz.ratio`) is symmetric, using a sorted tuple of normalized strings as a cache key halves the number of required expensive computations between unique pairs.

**Action:** Always pre-normalize and group unique values before performing exhaustive similarity comparisons. Implement result caching for symmetric similarity functions using sorted keys.
