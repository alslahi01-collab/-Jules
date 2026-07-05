## 2025-05-24 - Excel Comparison Optimization via Grouping and Caching
**Learning:** Replacing $O(N \times M)$ nested loops with unique value grouping and symmetric caching reduced matching time by ~20x for a 200x200 dataset. `df.to_dict('records')` is significantly faster than `df.iterrows()` for row-wise processing in tight loops.
**Action:** Always prefer grouping by unique values and caching expensive string similarity scores when performing cross-dataset comparisons.
