- time complexity grows linearly with two independent factors, multiply them to get the overall time complexity.

independent factors -> if you have two independent parts (outer loop and inner loop) of an algorithm, and each part has a linear time complexity, you multiply their complexity.

### Linear growth
if you you increase the input size by a factor, the execution time increases by the same factor.

Example -> you have an array of size N, and for each element in the array, you need to perform an operation that takes K steps. That's N operations, and each of those N operations takes K steps. The total number of steps is then `N * K`.

### LPS Array (in KMP) Longest Prefix Suffix
for each position `i` in the patterns, `LPS[i]` stores the length of the longest proper prefix that is also a suffix of the sub-string ``

### Recursion
- return address, return value, stack trace
- pre-operation (something done before recursion), Recursion (actual function call), Post-operation (something done after recursion).
- base case

> [!INFO]
> recursive function terminates by reaching a base case, where the function no longer calls itself and instead returns a specific value or performs a final operation.

> [!INFO]
> The call stack grows downward as recursive calls are made, then unwinds upward as each function returns its calculated value, with each function adding its own computation to the final result.