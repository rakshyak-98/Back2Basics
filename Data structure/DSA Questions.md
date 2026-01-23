[169 majority-element](https://leetcode.com/problems/majority-element/)
- pair different elements and discard them.
- only the majority element can remain at the end, because it's more frequent than all others combined.
- Boyer-Moore Majority Vote Algorithm.

---

[3494 Find the Minimum Amount of Time to Brew Potions](https://leetcode.com/problems/find-the-minimum-amount-of-time-to-brew-potions)

---

[977 Squares of sorted array](https://leetcode.com/problems/squares-of-a-sorted-array/description/)
- fill backward(end), two pointers start and end.
- if array is not sorted two pointers approach breaks - because it assumes order around 0.

---

[118 Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/)

---

[2273 Find Resultant Array After Removing Anagrams](https://leetcode.com/problems/find-resultant-array-after-removing-anagrams)

---

[15 3Sum](https://leetcode.com/problems/3sum/)
- Now it’s the **2-Sum** problem with target `-a`.  
- Known trick: sort + two-pointer
- Reduce to 2-sum -> `b + c = -a`
- Outer loop fix `i`  
- Inner while find pairs via 2-pointer

---

[Game of Life](https://leetcode.com/problems/game-of-life/description/)
- the eight coordinate pairs represent all possible moves from a cell in a grid.
	- they enumerate exactly 8 directions around a cell.

---

[Contiguous Array](https://leetcode.com/problems/contiguous-array/description/)
- Given a binary array `nums`, return _the maximum length of a contiguous subarray with an equal number of_ `0` _and_ `1`.

- What we need to know is. Same prefix sum at two indices = balanced subarray between them
- Longest subarray with target sum -> prefix sum + hash map.

---

[Longest common prefix](https://leetcode.com/problems/longest-common-prefix/submissions/1894187919/?envType=problem-list-v2&envId=wrdcuh52)

- The longest common prefix can never be longer then the shortest string in the array.
- Think of the strings as columns in a table. We're checking if each "row" has all the identical values.