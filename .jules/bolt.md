## 2025-05-22 - Excel Comparison Optimization
**Learning:** In row comparison loops, `df.iterrows()` and repeated `normalize_arabic` calls were the main bottlenecks. Pre-converting to records and using unique value grouping achieved ~35x speedup.
**Action:** Always prefer `df.to_dict('records')` for row iteration in high-frequency loops and group by unique values when doing O(N*M) comparisons.
