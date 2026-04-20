## 2025-05-15 - [Excel Row Matching Optimization]
**Learning:** The application had an $O(N \times M)$ bottleneck in `process_sheets` and `process_comparison` due to nested loops iterating over every row pair. The overhead was compounded by expensive `fuzz.ratio` calls and redundant `normalize_arabic` processing for identical strings across rows.

**Action:**
- Use `@lru_cache` for normalization functions to avoid redundant regex operations.
- Pre-calculate normalized values for the entire column to avoid repeated function calls in the inner loop.
- Use a hash-map (dictionary) to group row indices by their normalized values. This allows for $O(1)$ lookup of exact matches and ensures fuzzy matching is only performed once per unique string pair.
- Cache fuzzy matching results between unique string pairs using a symmetric key (e.g., `tuple(sorted((s1, s2)))`).
- Use lazy row conversion (e.g., `iloc[idx].to_dict()`) only when a match is found to save memory and CPU cycles.
