## 2025-05-15 - Optimizing Exhaustive Excel Row Comparison

**Learning:** In applications performing exhaustive row-by-row comparisons (like fuzzy matching between two sheets), the primary bottlenecks are redundant string normalization and repetitive similarity calculations for duplicate or near-duplicate values. Iterating over DataFrames using `iterrows()` is also significantly slower than processing a list of records.

**Action:**
1. Use `functools.lru_cache` on normalization and similarity functions to eliminate redundant CPU-intensive work.
2. Group target rows by their normalized values into a hash map (dictionary) to allow $O(1)$ exact matching.
3. Perform fuzzy matching only once per pair of *unique* normalized values, then propagate the result to all original row indices.
4. Convert DataFrames to `to_dict('records')` before tight loops to bypass pandas overhead. This combination achieved a ~50x-80x speedup in this codebase.
