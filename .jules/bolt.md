## 2025-05-15 - Optimized fuzzy matching with grouping and caching

**Learning:** In Excel comparison tasks, row-by-row iteration using `df.iterrows()` and repeated `fuzz.ratio` calls on redundant data is the primary bottleneck. Grouping row indices by unique normalized values allows performing expensive fuzzy matching once per value pair instead of once per row pair, reducing complexity from $O(N \times M)$ to $O(U_1 \times U_2)$. Pre-converting DataFrames to records (`to_dict('records')`) also significantly reduces access overhead inside high-frequency loops.

**Action:** Always group by unique values before performing $O(N^2)$ operations like fuzzy matching. Use `lru_cache` for normalization functions and symmetric caching (sorted tuple keys) for similarity scores. Pre-convert DataFrames to list of dicts to avoid pandas overhead in loops.
