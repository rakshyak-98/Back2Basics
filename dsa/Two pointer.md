
- Each step resolves one conflict (too big / too small) deterministically.
- Eliminates dominated states: once a pointer moves, all skipped states are provably invalid.

> Monotonic property -> A property is monotonic if it changes in only one direction (once it increases, it never decreases or vice versa).
- this enables one-way decisions.

**When it fails**
- Unsorted data with no monotonic rule.
- Global constraints needing lookahead.
- Multiple independent conditions.

**Edge cases**
- Equal values → non-strict monotonicity.
- Floating-point precision breaks monotonic checks.
- Data mutation invalidates monotonic assumptions.

**Sorted two pointer array**
- Ordered values let us decide which way to move pointer. 
- After sorting, same value repeated → skip to prevent same triplet.

## Two pointer: pointer placement rules

### Pointer at first + last
- use when global comparison across range is needed.
- Decision depends on sum/difference/ordering of two elements.
- You want to shrink search space from both side.

**Movement rule**
- Compare `a[l]` and `a[r]`
- Move **one pointer inward** based on condition
- Each move strictly reduces range → O(n)

### Pointer at first + next
- use when local adjacency/pair enumeration in needed.
- Need to examine all pairs in order.
- One pointer is anchor, other explores ahead.
- Window grows/slides forward.

**Movement rule**
- Fix `i`
- Move `j` forward
- When condition breaks → move `i`, reset or adjust `j`

```text
Initialize pointers p1, p2
while pointers within bounds:
  evaluate condition using p1, p2
  move exactly one (or both) pointers based on monotonic rule
  maintain invariant

```

## Converging pointers (opposite ends)

```js
function twoSumSorted(arr, target) {
  let l = 0
  let r = arr.length - 1

  while (l < r) {
    const sum = arr[l] + arr[r]
    if (sum === target) return [l, r]
    if (sum > target) r--
    else l++
  }

  return []
}
```

## Sliding window (same direction)

```js
function twoSumSorted(arr, target) {
  let l = 0
  let r = arr.length - 1

  while (l < r) {
    const sum = arr[l] + arr[r]
    if (sum === target) return [l, r]
    if (sum > target) r--
    else l++
  }

  return []
}

```

## Fast and slow pointers

```js
function removeDuplicates(nums) {
  let slow = 0

  for (let fast = 0; fast < nums.length; fast++) {
    if (fast === 0 || nums[fast] !== nums[fast - 1]) {
      nums[slow] = nums[fast]
      slow++
    }
  }

  return slow
}

```

