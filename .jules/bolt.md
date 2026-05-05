## 2025-05-15 - [Initial Bottleneck Identification]
**Learning:** The row comparison logic in `process_sheets` uses a nested O(N*M) loop with expensive fuzzy matching and redundant string normalization. For 500x500 rows, this takes ~27 seconds.
**Action:** Implement LRU caching for normalization, unique value grouping to reduce redundant fuzzy calculations, and symmetric similarity caching.
