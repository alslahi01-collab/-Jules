# Bolt Performance Journal

## 2025-05-15 - Initial Performance Baseline
**Learning:** The current implementation uses O(N*M) row comparisons with expensive regex-based normalization and fuzzy matching inside nested loops. In a 200x200 row comparison, this takes ~4.4s.
**Action:** Implement lru_cache for normalization, use hash-maps for exact matches to skip O(N*M) iterations where possible, and cache fuzzy match results for unique string pairs.
