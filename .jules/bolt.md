## 2025-05-22 - [Pre-normalization of data in nested loops]
**Learning:** Redundant operations like string normalization inside nested loops lead to O(N*M) complexity for tasks that could be O(N+M). Pre-calculating these values significantly reduces CPU cycles.
**Action:** Always check if values processed in loops can be pre-calculated or cached.
