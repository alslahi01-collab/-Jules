## 2025-05-22 - [Optimizing Fuzzy Matching in Excel Comparisons]
**Learning:** The primary bottleneck was the O(N*M) complexity of nested row loops combined with expensive `fuzz.ratio` calls and `df.iterrows()` / `row.to_dict()` overhead. Accessing row data inside the inner loop was significantly slower than pre-converting the DataFrame to a list of records. Furthermore, redundant fuzzy matching of identical string pairs across many rows caused massive unnecessary computation.

**Action:**
1. Always pre-convert DataFrames to lists of records (`df.to_dict('records')`) before tight loops.
2. Reduce O(N*M) to O(U1*U2) by grouping row indices by unique normalized values.
3. Cache results of expensive similarity functions (like `fuzz.ratio`) using unique value pairs as keys.
4. Use `@functools.lru_cache` for repetitive string normalization functions.
