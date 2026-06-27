## 2025-05-15 - [Excel Matching Logic Optimization]
**Learning:** In applications performing row-by-row fuzzy matching across large Excel sheets, the standard O(N*M) approach using `df.iterrows()` and repeated `fuzz.ratio` calls on redundant strings is the primary performance bottleneck.
**Action:** Replace `iterrows()` with `.to_dict('records')` for faster access, and group row indices by unique normalized values to perform fuzzy matching only once per unique string pair, using a symmetric results cache to halve the remaining unique-pair computations.
