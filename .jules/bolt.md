## 2025-01-24 - Initial Performance Assessment
**Learning:** The current Excel comparison logic uses an O(N*M) nested loop with redundant string normalization and slow `iterrows()` calls. Fuzzy matching is performed even for pairs that could be pre-filtered.
**Action:** Implement pre-normalization, use dictionaries for exact matches, and iterate over unique values for fuzzy matching to reduce complexity to O(U1*U2).
