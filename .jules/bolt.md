## 2025-05-14 - Optimized Symmetric Similarity Caching

**Learning:** When performing exhaustive N x M row comparisons using similarity metrics like `fuzz.ratio`, the number of calls to the expensive similarity function can be significantly reduced by grouping rows by unique values and caching the result of the similarity computation for each unique pair. Furthermore, since similarity metrics are often symmetric, using a sorted tuple of unique values as a cache key halves the number of required computations.

**Action:** In any row comparison logic, always group indices by unique values first. Perform the expensive similarity check only once per unique value pair and cache it symmetrically.
