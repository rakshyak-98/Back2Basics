[pivot index](https://leetcode.com/problems/find-pivot-index/)
- pre-compute the total sum
- `lhs === total sum - lhs - nums[i]`

### Prefix sum balance checking
- Find index where left part = right part
- split array evenly
- find equilibrium point
- this trick is always: pre computer total, then compare with running prefix.

[169 majority-element](https://leetcode.com/problems/majority-element/)
- pair different elements and throw them away.
- only the majority element can remain at the end, because it's more frequent than all others combined.
- Boyer-Moore Majority Vote Algorithm.

## Cancellation trick
- When you need to find an element that dominates, you can cancel out minority elements until only the dominant remains.