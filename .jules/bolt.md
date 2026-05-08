## 2025-05-14 - Optimized Row Comparison with Unique-Value Grouping and Symmetric Similarity Caching
**Learning:** O(N*M) row-by-row fuzzy comparison in Excel matching tools is a major bottleneck. Grouping row indices by unique normalized values and caching symmetric similarity results (e.g., fuzz.ratio) achieves massive speedups, especially with duplicate data.
**Action:** Use dictionary-based index grouping and symmetric result caching for any pairwise similarity comparison tasks.
