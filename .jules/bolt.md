## 2025-05-14 - Initial Bottleneck Analysis
**Learning:** The core Excel comparison logic used O(N*M) nested loops with expensive `fuzz.ratio` and `normalize_arabic` calls on every iteration. Row access via `df.iterrows()` and `row.to_dict()` inside the inner loop was also a significant overhead.
**Action:** Use `df.to_dict('records')` for zero-overhead row access. Group indices by unique normalized values to perform fuzzy matching once per unique value pair. Cache `normalize_arabic` and fuzzy results to minimize redundant computations.
