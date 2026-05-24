## 2025-05-22 - [Optimizing Row Comparison and Fuzzy Matching]
**Learning:** In high-frequency fuzzy matching loops (like comparing Excel rows), the bottleneck is often a combination of:
1. Inefficient row access via `df.iterrows()`.
2. Redundant string normalization.
3. Redundant $O(N \times M)$ calls to expensive similarity functions like `fuzz.ratio` for identical or repeating values.
4. Redundant I/O when reading the same Excel sheet multiple times in nested loops.

**Action:**
1. Use `df.to_dict('records')` for faster record-based iteration.
2. Use `@lru_cache` for normalization functions.
3. Group indices by unique normalized values into a dictionary (`norm_map`). This enables $O(1)$ exact matches and reduces fuzzy matching complexity from $O(N \times M)$ to $O(U_1 \times U_2)$ where $U$ is the number of unique values.
4. Cache fuzzy matching results for symmetric pairs `tuple(sorted((v1, v2)))`.
5. Pre-read and pre-process all target sheets into memory once outside the comparison loops.
