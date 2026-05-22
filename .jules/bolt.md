## 2025-05-22 - Dataframe Iteration and Value Grouping
**Learning:** Using `df.iterrows()` or accessing rows by index inside nested loops is a major bottleneck in Pandas. Pre-converting DataFrames to lists of dictionaries (`to_dict('records')`) and grouping row indices by unique normalized values allows reducing comparison complexity from O(N*M) to O(U1*U2) and makes row access nearly instantaneous.
**Action:** Always pre-convert DataFrames to records and use dictionary-based grouping for high-frequency row comparisons.

## 2025-05-22 - Symmetry in Similarity Caching
**Learning:** For symmetric similarity functions like `fuzz.ratio(a, b)`, using a sorted tuple `tuple(sorted((a, b)))` as a cache key effectively halves the number of required computations between unique string pairs.
**Action:** Use sorted tuples for caching symmetric relationship results to optimize O(N^2) processes.
