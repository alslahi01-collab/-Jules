## 2025-05-14 - Initial Assessment
**Learning:** The application performs O(N*M) row comparisons with redundant Arabic text normalization and fuzzy matching.
**Action:** Use lru_cache for normalization and a hash-map based approach for exact matches to reduce complexity.
