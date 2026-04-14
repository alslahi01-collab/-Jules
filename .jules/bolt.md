## 2025-05-15 - Excel Comparison Bottleneck
**Learning:** The O(N*M) nested loop for comparing Excel rows was extremely slow due to redundant string normalization and repeated fuzzy matching calls. In a 150x150 comparison, it took ~8.16s.
**Action:** Use pre-normalization of columns before entering comparison loops and a hash map (dictionary) for O(1) exact matching lookups. Additionally, use `functools.lru_cache` for the normalization function. These optimizations reduced the comparison time to ~0.12s, a ~98% improvement.
