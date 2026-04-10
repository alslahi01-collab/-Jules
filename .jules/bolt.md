## 2025-05-22 - [Excel Comparison Optimization]
**Learning:** The O(N*M) nested loop for row comparison was performing redundant string normalization and fuzzy score calculations. Pre-calculating normalized values and using a hash map for exact matches, combined with LRU caching for fuzzy scores, drastically improves performance.
**Action:** Use dictionaries for O(1) exact matches and `functools.lru_cache` for expensive fuzzy matching in nested loops.
