## 2025-05-14 - Initial Performance Assessment
**Learning:** The core Excel comparison logic uses a nested O(N*M) loop with expensive string normalization and fuzzy matching inside the inner loop. 500x500 rows take ~28s.
**Action:** Implement pre-calculation of normalized values, group by unique values to reduce fuzzy matching calls, and use `lru_cache` for normalization and similarity results.
