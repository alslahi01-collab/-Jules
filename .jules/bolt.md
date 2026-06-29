## 2026-06-29 - Optimization of Excel Comparison Logic
**Learning:** In Excel comparison tasks with high duplication or many-to-many match potential, replacing O(N*M) nested loops with a grouped-unique-value approach (O(U1*U2)) and symmetric fuzzy caching provides massive speedups (approx 10-20x for 200x200 rows). Using `df.to_dict('records')` is significantly faster than `df.iterrows()` for row-wise iteration in these loops.
**Action:** Always prefer grouping identical values and caching results of expensive similarity scores (like fuzz.ratio) when comparing large datasets.
