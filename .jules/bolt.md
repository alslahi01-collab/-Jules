## 2025-05-14 - Optimized Excel comparison logic with caching and dictionary grouping

**Learning:** The previous implementation of row comparison was O(N*M) where N and M are the number of rows in each sheet. Inside the nested loop, it performed string normalization and fuzzy matching repeatedly for identical values. By pre-normalizing columns, grouping row indices by their normalized value in a dictionary, and caching fuzzy ratios for unique string pairs, we reduced the complexity significantly and avoided redundant computations.

**Action:** Always pre-calculate expensive operations (like normalization) outside of nested loops and use dictionaries to map unique values to indices for O(1) matching and O(unique_pairs) fuzzy matching.
