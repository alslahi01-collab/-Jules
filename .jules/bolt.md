## 2025-05-15 - [DataFrame Row Access Bottleneck]
**Learning:** In high-frequency fuzzy matching loops, using `df.iloc[idx]` or `row.to_dict()` inside the inner match condition is a massive performance killer. Pre-converting the DataFrame to a dictionary using `df.to_dict('records')` outside the loop reduces row access overhead to nearly zero.
**Action:** Always pre-convert DataFrames to list of dicts (records) or similar lightweight structures before entering nested loops or frequent access paths.

## 2025-05-15 - [Unique Value Grouping for Fuzzy Matching]
**Learning:** When performing O(N*M) fuzzy comparisons, grouping indices by unique normalized values and iterating only over unique pairs reduces complexity to O(U1*U2). This is critical when datasets contain many duplicate or similar values.
**Action:** Use a dictionary to map unique normalized strings to lists of row indices for the target dataset.
