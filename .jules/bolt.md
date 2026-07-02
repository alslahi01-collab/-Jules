## 2025-05-15 - [Excel Matching Logic Optimization]
**Learning:** Refactoring nested row comparison loops by grouping identical normalized values significantly improves performance. However, when both source and target indices are needed for parity with $O(N \times M)$ logic (where one entry is appended per row-pair match), ensure nested loops iterate over both `indices1` and `indices2`.
**Action:** Always verify match counts against a baseline when changing complexity from $O(N \times M)$ to a grouping-based approach.
