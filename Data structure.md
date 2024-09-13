## Array
- deleting an element from the array can be done in O(1) by swapping the element to be deleted with the last element in the array and then removing the last element.

### Sub-array
- a sub-array is a contiguous segment of an array. For an array of size N, a sub-array can start at any index from 0 to N -1. 
- counting sub-array : from each start index i (where i ranges from 0 to N - 1), the sub-array can end at any index j (where j ranges from i to N - 1).
- the number of choices from the ending index j for a given starting index i in N - i.

### Prefix sum
- allow for quick calculations of the sum of elements within a specific range of an array.
- Efficient Range queries : sum(L, R) = prefix[R] - prefix[L-1]. This is significantly faster than recalculating the sum from scratch, which would take O(n) time for each query.
- used in algorithms for finding the number of elements less than or equal to a given value.

### Sliding window
1. Maximum Sum Subarray of Size K 