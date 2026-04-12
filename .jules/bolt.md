## 2026-04-12 - Excel Comparison Loop Optimization
**Learning:** Found a critical O(N*M) bottleneck in the Excel comparison logic. String normalization and fuzzy matching were performed inside nested loops for every row pair. Using dictionaries to group rows by their normalized values allows for O(1) exact matches and reduces fuzzy matching complexity to O(U1*U2) where U is the number of unique strings.

**Action:** Always pre-calculate normalized values using Pandas `.apply()` and use dictionaries to map unique values to row indices before entering comparison loops.
