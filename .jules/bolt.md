## 2025-05-14 - [Row Comparison Optimization]
**Learning:** The O(N*M) row-by-row comparison logic with redundant Arabic normalization and fuzzy matching was the primary bottleneck. For a 500x500 comparison (250,000 pairs), the original implementation took ~32s.
**Action:** Implemented grouping of row indices by unique normalized values and used a symmetric similarity result cache. This reduced the complexity to O(U1*U2) and avoided redundant fuzzy matching. Resulted in a ~12.7x speedup (~2.5s for 500x500 rows) while maintaining 100% result accuracy.
