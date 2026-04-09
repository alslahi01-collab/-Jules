## 2025-05-14 - [O(1) Dictionary Lookup for Excel Comparison]
**Learning:** The previous implementation used $O(N \cdot M)$ nested loops for both exact and fuzzy matching. By pre-calculating normalized values and using a dictionary to map normalized strings to row indices, exact matches are reduced to $O(N)$ overall ($O(1)$ per row). Additionally, caching `fuzz.ratio` results with `lru_cache` significantly speeds up fuzzy matching when data contains duplicates or frequent similar patterns.
**Action:** Use dictionary mappings for exact matches and `functools.lru_cache` for fuzzy metrics in any similarity-matching tasks.

## 2025-05-14 - [Pre-processing multi-sheet workbooks]
**Learning:** In the Streamlit app, File 2 was being re-read from memory/disk for every sheet in File 1. Pre-processing all sheets of File 2 into a list of dictionaries before the main loop avoids redundant I/O and re-normalization.
**Action:** Always pre-process the "target" dataset into an optimized in-memory format when performing nested comparisons across multiple containers (like Excel sheets).
