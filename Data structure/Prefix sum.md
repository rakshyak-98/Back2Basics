> [!INFO]
> - Prefix sum tells you total count of element in an array.

> [!NOTE]
> - sum(L, R) = prefix[R] - prefix[L-1].
> - This is significantly faster than recalculating the sum from scratch, which would take O(n) time for each query.

- allow for quick calculations of the sum of elements within a specific range of an array.
- used in algorithms for finding the number of elements less than or equal to a given value.