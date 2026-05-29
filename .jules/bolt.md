## 2025-01-24 - Initial Performance Audit
**Learning:** The core bottleneck in both Flask and Streamlit apps is the O(N*M) nested loop for row comparison. It performs redundant Arabic normalization and expensive fuzzy matching for every row pair.
**Action:** Optimize row comparison by pre-calculating normalized values, using hash maps for exact matches, and performing fuzzy matching only on unique value pairs.

## 2025-01-24 - Pandas `iterrows()` and `iloc` Bottlenecks
**Learning:** In high-frequency comparison loops (like $O(N \times M)$ fuzzy matching), accessing Pandas rows via `iterrows()` or `iloc` inside the inner loop is extremely slow. Pre-converting DataFrames to a list of dictionaries using `df.to_dict('records')` outside the loops can yield a 10x-50x speedup alone.
**Action:** Always pre-convert DataFrames to records or NumPy arrays before entering performance-critical nested loops.
