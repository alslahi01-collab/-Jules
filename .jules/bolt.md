## 2025-05-14 - Initial Performance Audit
**Learning:** The application performs O(N*M) string comparisons using fuzzy matching in nested loops. For 100x100 rows, it takes ~2.1s. This will scale poorly for larger datasets (e.g., 1000x1000 would take ~200s).
**Action:** Implement lru_cache for normalization and group unique values to reduce the number of fuzzy matching calls from O(N*M) to O(U1*U2) where U is unique values.

## 2025-05-14 - Optimized Row Comparison with Unique-Value Grouping
**Learning:** In Excel comparison tasks, rows often contain duplicate values or values that normalize to the same string. Grouping row indices by unique normalized values reduces the complexity of expensive fuzzy matching from O(N*M) to O(U1*U2), where U is the number of unique values.
**Action:** Use a dictionary (hash map) to group indices of rows sharing the same normalized value. Perform fuzzy matching once per unique value pair and use symmetric caching (sorted tuple keys) to further halve computation. This yielded a ~4.7x speedup on 100x100 datasets with duplicates.
