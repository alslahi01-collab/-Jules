## 2025-05-14 - [Initial Optimization Plan]
**Learning:** The application performs O(N*M) fuzzy string comparisons using `thefuzz.fuzz.ratio` in a nested loop over Excel rows. `df.iterrows()` and repeated `row.to_dict()` calls inside the inner loop are major bottlenecks.
**Action:** Use `df.to_dict('records')` for faster access, cache normalized strings, and group rows by unique normalized values to reduce `fuzz.ratio` calls from O(N*M) to O(U1*U2).
