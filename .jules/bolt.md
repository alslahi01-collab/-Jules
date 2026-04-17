## 2025-05-15 - O(N*M) Comparison Bottleneck
**Learning:** The current comparison logic in `app.py` and `streamlit_app.py` uses nested loops (`iterrows`) with redundant string normalization and fuzzy matching. For a 100x100 comparison, this leads to 10,000 fuzzy match calls even if many strings are identical or have been seen before.
**Action:** Implement `functools.lru_cache` for normalization and fuzzy matching, and use hash maps (dictionaries) for O(1) exact matches to bypass the nested loop for identical values.

## 2025-05-15 - Exact Match Logic Constraint
**Learning:** To ensure zero behavioral regressions, an exact match for a specific row pair should not prevent checking for fuzzy matches against other non-identical rows if the original logic was exhaustive. Initially, I used `continue` after an exact match, which caused fewer results than the baseline.
**Action:** Remove `continue` after exact match blocks and instead use a guard like `if norm1 == norm2_val: continue` inside the fuzzy matching loop to ensure all relevant pairs are checked exactly once while skipping redundant fuzzy calculations for already matched identical strings.
