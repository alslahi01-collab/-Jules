## 2025-05-14 - Pre-calculate expensive operations in nested loops
**Learning:** Pre-calculating operations like string normalization (Arabic normalization) outside of nested O(N*M) loops and using `enumerate()` instead of `iterrows()` for DataFrame row processing provides significant performance gains (over 90% in benchmarks).
**Action:** Always look for redundant calculations inside nested loops, especially string operations and DataFrame accessors.
