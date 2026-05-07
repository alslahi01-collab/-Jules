## 2025-05-14 - Optimized Row Comparison with Unique-Value Grouping and Symmetric Caching

**Learning:** The core performance bottleneck was the O(N*M) nested loop that repeatedly performed expensive fuzzy similarity matching on identical strings and redundant pairs. By grouping row indices by their normalized values, we reduced the complexity to O(U1*U2) where U is the number of unique values. Caching the results of `normalize_arabic` and `fuzz.ratio` between unique pairs further minimized computation.

**Action:** Always look for O(N^2) loops involving expensive string processing. Use dictionaries to group indices of duplicate values and perform expensive matches only once per unique pair. Cache symmetric operations (like similarity) using sorted tuples of keys.
