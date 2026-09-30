- Why zero-based indexing -> primarily due to memory efficiency and pointer arithmetic in lower level implementation like C, which influenced most modern languages.

Offset from Base Address -> Arrays are stored in contiguous memory blocks. The first element is the array's base address (offset 0). To access the i-th element, the compiler simply computes `base + i * element_size` no subtraction needed.

> [!NOTE]
> A 1-based index require `base + (i - 1) * element_size`, adding an unnecessary operation that slows things down, especially in loops or large-scale access.

## Index computations
**an index is usually derived from one of five things, position, distance, boundary, transformation or arithmetic mapping.**

1. **Direct positional computation** The simplest case is when the required index comes directly from another index.
```txt
nums = [10, 20, 30, 40, 50]
index:  0   1   2   3   4
```

common computations:
```txt
i + 1       // next index
i - 1       // previous index
i + k       // k positions forward
i - k       // k positions backward
```
but you must check bounds
```go
if i+1 < len(nums) {
	// nums[i+1]
}
```

2. **Relative index/offset computation** A very common pattern is converting a position into a position relative to some boundary.
```txt
left ........ right
  2             5
```
then the window size `right - left + 1` why `+1` because both endpoints are included.

3. **Distance-from-end computation** Sometimes you need to convert an index measured from the beginning into an index measured from the end.
```txt
nums = [10, 20, 30, 40, 50]
index:  0   1   2   3   4
```
the reverse index is:
```go
len(nums) - 1 - i
```

4. **Circular index computation** This is one of the most important index formulas.
```go
next := (i + 1) % n
```

```txt
n = 5

0 → 1
1 → 2
2 → 3
3 → 4
4 → 0
```
similarly:
```go
previous := (i - 1 + n) % n
```
**The `+n` prevents a negative result.**

5. **Rotation index computation** Array rotation is essentially circular indexing.
Rotate right by `k=2`. The element originally at index `i` move to:
```go
nums := [1, 2, 3, 4, 5] 
k := 2
newRightIndex := (i+k)%n
newLeftIndex := (i-k+n)%n
```