# Bolt Performance Journal ⚡

## 2026-04-16 - Optimized Excel Comparison Logic
**Learning:** The previous implementation had $O(N \times M)$ complexity for row comparisons, with redundant string normalizations and expensive `fuzz.ratio` calls. By grouping row indices by their normalized values into a dictionary, we can perform fuzzy matching once per unique value pair instead of once per row pair. Additionally, `functools.lru_cache` on normalization and fuzzy matching functions significantly reduces CPU cycles for repeated inputs.

**Action:**
1. Use `norm_map = {}` to group row indices by normalized values: `norm_map.setdefault(norm, []).append(idx)`.
2. Apply `@lru_cache` to expensive string processing and similarity functions.
3. Pre-convert DataFrames to dictionaries with `to_dict('index')` for faster row access compared to `iloc` in tight loops.
