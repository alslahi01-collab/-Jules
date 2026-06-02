## 2025-05-22 - Optimized Row Comparison Engine

**Learning:** In high-frequency fuzzy matching loops, using `df.iterrows()` or `row.to_dict()` inside the inner match condition is a massive performance killer. Pre-converting the DataFrame to a list of dictionaries using `df.to_dict('records')` outside the loop reduces row access overhead to nearly zero. Additionally, grouping row indices by unique normalized values allows performing fuzzy matching once per unique value pair instead of once per row pair, significantly reducing expensive `fuzz.ratio` calls.

**Action:** Always pre-process DataFrames into records and group by unique comparison values when performing O(N²) or O(N*M) matching operations. Cache result scores for unique value pairs.
