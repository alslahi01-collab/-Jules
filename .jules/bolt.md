## 2025-05-15 - Optimized Excel Comparison
**Learning:** Nested loops comparing normalized strings are extremely slow when normalization and fuzzy matching are repeated millions of times. Pre-calculating normalized values and using dictionary lookups for exact matches provides a massive speedup (30x-60x).
**Action:** Always pre-calculate expensive string transformations outside of nested loops and use hash maps for exact matching before falling back to fuzzy algorithms.
