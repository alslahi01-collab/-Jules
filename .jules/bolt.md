## 2025-05-22 - [Optimizing Nested Loops with Unique Value Grouping]
**Learning:** In row-by-row comparison tasks (like Excel matching), the `iterrows()` method combined with redundant string normalization and fuzzy matching is an O(N*M) bottleneck.
**Action:**
1. Pre-convert DataFrames to list of dicts (`to_dict('records')`) to avoid `df.iloc` overhead.
2. Group row indices by unique normalized values in a hash map.
3. Perform normalization and fuzzy matching once per unique value/pair.
4. Cache fuzzy results between unique pairs to avoid re-computation.
5. In multi-sheet comparisons, pre-process all target sheets into memory to avoid redundant I/O in nested loops.
