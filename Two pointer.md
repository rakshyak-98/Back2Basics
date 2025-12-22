
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