## 2026-04-25 - Optimized row comparison
**Learning:** Row-by-row comparison with string normalization and fuzzy matching is a major bottleneck (O(N^2)). Using lru_cache for normalization and a results cache for fuzzy matching significantly reduces overhead. Grouping rows by normalized values allows for O(1) exact matches and reduces the number of fuzzy comparisons when values are non-unique.
**Action:** Always use caching for expensive string operations and fuzzy matching in loops. Prefer dictionary lookups for exact matches before falling back to fuzzy logic.
