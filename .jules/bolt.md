# Bolt's Performance Journal ⚡

## 2025-05-15 - Initial Assessment
**Learning:** The core bottleneck is the $O(N \times M)$ nested loop for row comparison, where expensive `normalize_arabic` (regex-heavy) and `fuzz.ratio` (Levenshtein distance) are called repeatedly. Redundant normalization and redundant fuzzy matching on duplicate strings are major targets.
**Action:** Implement pre-normalization, memoization for normalization, and group unique values to reduce the number of fuzzy comparisons from $O(N \times M)$ to $O(U_1 \times U_2)$.
