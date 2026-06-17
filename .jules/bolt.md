## 2026-06-17 - Algorithmic Optimization for Fuzzy Matching

**Learning:** Naive $O(N \times M)$ fuzzy matching using `df.iterrows()` and repeated `fuzz.ratio` calls is extremely slow. By pre-converting DataFrames to records, grouping indices by unique normalized values, and caching `fuzz.ratio` results for string pairs, complexity is reduced to $O(U1 \times U2)$ where $U$ is the number of unique strings. This achieved a ~52x speedup in this codebase.

**Action:** Always group target data by unique keys and use a result cache for expensive similarity metrics like `fuzz.ratio` to avoid redundant computations on duplicate or repeated values.

## 2026-06-17 - Streamlit Module Import Protection

**Learning:** Streamlit executes the entire script on run. Wrapping UI components in `if __name__ == "__main__":` is critical when you need to import logic functions (like `process_comparison`) into verification or benchmark scripts without triggering the Streamlit server or missing context errors.

**Action:** Encapsulate Streamlit UI code in main blocks to enable modular testing of the underlying business logic.
