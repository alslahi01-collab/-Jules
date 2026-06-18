## 2026-06-18 - [Fuzzy Matching Complexity Reduction]
**Learning:** For Excel row comparison involving fuzzy matching, O(N*M) complexity can be reduced to O(U1*U2) by grouping row indices by unique normalized values. Combined with record-based iteration and symmetry-aware fuzzy results caching, this yields >10x speedup on typical datasets.
**Action:** Use dictionary-based index grouping and pre-cached fuzzy scores when comparing large datasets in the future.
