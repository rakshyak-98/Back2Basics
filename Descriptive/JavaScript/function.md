- you can add custom properties to your functions at any  time.


`flatMap` -> it maps each element using a function, then flatten the result by one level.

```js
const arr = [1, 2, 3];

// Using map (returns nested arrays)
const mapped = arr.map(x => [x, x * 2]);
console.log(mapped);
// [[1, 2], [2, 4], [3, 6]] ❌ Nested!

// Using flatMap (flattens automatically)
const flatMapped = arr.flatMap(x => [x, x * 2]);
console.log(flatMapped);
// [1, 2, 2, 4, 3, 6] ✅ Flat!
```