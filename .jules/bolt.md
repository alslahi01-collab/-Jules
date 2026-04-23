## 2025-05-14 - Initial Performance Assessment
**Learning:** The application performs a nested O(N*M) loop for fuzzy string comparison, calling normalization and fuzzy matching functions repeatedly even for identical string values. This is the primary bottleneck for large Excel files.
**Action:** Implement lru_cache for normalization, use hash-maps for exact matches, and iterate over unique values for fuzzy matching to minimize redundant computations.
