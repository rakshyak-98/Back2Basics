
Given an array of **positive** integers **arr[]**, return the **second largest** element from the array. If the second largest element doesn't exist then return **-1.**

Note: The second largest element should not be equal to the largest element.

**Examples:**

**Input:** arr[] = [12, 35, 1, 10, 34, 1]
**Output:** 34
**Explanation:** The largest element of the array is 35 and the second largest element is 34.

**Input:** arr[] = [10, 5, 10]
**Output:** 5
**Explanation:** The largest element of the array is 10 and the second largest element is 5.

**Input:** arr[] = [10, 10, 10]
**Output:** -1
**Explanation:** The largest element of the array is 10 and the second largest element does not exist.

**Constraints:**  
2 ≤ arr.size() ≤ 105  
1 ≤ arr[i] ≤ 105

---

### Move All Zeroes to End

Given an array **arr[]**. Push all the zeros of the given array to the right end of the array while maintaining the order of non-zero elements. Do the mentioned change in the **array in place**.

**Examples:**

**Input:** arr[] = [1, 2, 0, 4, 3, 0, 5, 0]
**Output:** [1, 2, 4, 3, 5, 0, 0, 0]
**Explanation:** There are three 0s that are moved to the end.

**Input:** arr[] = [10, 20, 30]
**Output:** [10, 20, 30]
**Explanation:** No change in array as there are no 0s.

**Input:** arr[] = [0, 0]
**Output:** [0, 0]
**Explanation:** No change in array as there are all 0s.

**Constraints:**  
1 ≤ arr.size() ≤ 105  
0 ≤ arr[i] ≤ 10

---

### Reverse an Array

You are given an array of integers **arr[]**. Your task is to **reverse** the given array.

**Examples:  
**

**Input:** arr = [1, 4, 3, 2, 6, 5]
**Output:** [5, 6, 2, 3, 4, 1]  
**Explanation:** The elements of the array are 1 4 3 2 6 5. After reversing the array, the first element goes to the last position, the second element goes to the second last position and so on. Hence, the answer is 5 6 2 3 4 1.

**Input**: arr = [4, 5, 2]
**Output:** [2, 5, 4]  
**Explanation:** The elements of the array are 4 5 2. The reversed array will be 2 5 4.  

**Input**: arr = [1]
**Output:** [1]  
**Explanation:** The array has only single element, hence the reversed array is same as the original.

**Constraints:  
**1<=arr.size()<=105  
0<=arr[i]<=105

---

### Rotate Array

Given an unsorted array _arr[]__**.**_ Rotate the array to the left (counter-clockwise direction) by _d_ steps, where _d_ is a positive integer. Do the mentioned change in the **array in place**.

Note: Consider the array as circular.

**Examples :  
**

**Input:** arr[] = [1, 2, 3, 4, 5], d = 2
**Output:** [3, 4, 5, 1, 2]
**Explanation:** when rotated by 2 elements, it becomes 3 4 5 1 2.

**Input:** arr[] = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], d = 3
**Output:** [8, 10, 12, 14, 16, 18, 20, 2, 4, 6]
**Explanation:** when rotated by 3 elements, it becomes 8 10 12 14 16 18 20 2 4 6.  

**Input:** arr[] = [7, 3, 9, 1], d = 9
**Output:** [3, 9, 1, 7]
**Explanation:** when we rotate 9 times, we'll get 3 9 1 7 as resultant array.

**Constraints:**  
1 <= arr.size(), d <= 105  
0 <= arr[i] <= 105

---

### Next Permutation

Given an array of integers **arr[]** representing a permutation, implement the **next permutation** that rearranges the numbers into the lexicographically next greater permutation. If no such permutation exists, rearrange the numbers into the lowest possible order (i.e., sorted in ascending order). 

Note - A permutation of an array of integers refers to a specific arrangement of its elements in a sequence or linear order.

**Examples:**

**Input:** arr = [2, 4, 1, 7, 5, 0]
**Output:** [2, 4, 5, 0, 1, 7]
**Explanation:** The next permutation of the given array is {2, 4, 5, 0, 1, 7}.

**Input:** arr = [3, 2, 1]
**Output:** [1, 2, 3]
**Explanation:** As arr[] is the last permutation, the next permutation is the lowest one.  

**Input:** arr = [3, 4, 2, 5, 1]
**Output:** [3, 4, 5, 1, 2]
**Explanation:** The next permutation of the given array is {3, 4, 5, 1, 2}.

**Constraints:**  
1 ≤ arr.size() ≤ 105  
1 ≤ arr[i] ≤ 105

---

### Majority Element

You are given an array of integer **arr[]** where each number represents a vote to a candidate. Return the candidates that have votes greater than one-third of the total votes, If there's not a majority vote, return an empty array. 

**Note:** The answer should be returned in an increasing format.

**Examples:**

**Input:** arr[] = [2, 1, 5, 5, 5, 5, 6, 6, 6, 6, 6]
**Output:** [5, 6]
**Explanation:** 5 and 6 occur more n/3 times.

**Input:** arr[] = [1, 2, 3, 4, 5]
**Output:** []  
**Explanation:** no candidate occur more than n/3 times.

**Constraint:**  
1 <= arr.size() <= 106  
-109 <= arr[i] <= 109

---

### Stock Buy and Sell - Multiple Transaction Allowed

The cost of stock on each day is given in an array **price[]**. Each day you may decide to either buy or sell the stock i at **price[i]**, you can even buy and sell the stock on the same day. Find the **maximum profit** that you can get.

Note: A stock can only be sold if it has been bought previously and multiple stocks cannot be held on any given day.

**Examples:**

**Input:** prices[] = [100, 180, 260, 310, 40, 535, 695]  
**Output:** 865  
**Explanation:** Buy the stock on day 0 and sell it on day 3 => 310 – 100 = 210. Buy the stock on day 4 and sell it on day 6 => 695 – 40 = 655. Maximum Profit = 210 + 655 = 865.  
![](https://media.geeksforgeeks.org/img-practice/prod/addEditProblem/878914/Web/Other/blobid2_1731054745.png)  
  
**Input:** prices[] = [4, 2, 2, 2, 4]  
**Output:** 2  
**Explanation:** Buy the stock on day 3 and sell it on day 4 => 4 – 2 = 2. Maximum Profit = 2.

**Constraints:**  
1 <= prices.size() <= 105  
0 <= prices[i] <= 104

---

### Stock Buy and Sell - Max one Transaction Allowed

Given an array **prices[]** of length n, representing the prices of the stocks on different days. The task is to find the maximum profit possible by buying and selling the stocks on different days when at most one transaction is allowed. Here one transaction means 1 buy + 1 Sell. If it is not possible to make a profit then **return 0**.

Note: Stock must be bought before being sold.

**Examples:**

**Input:** prices[] = [7, 10, 1, 3, 6, 9, 2]  
**Output:** 8**Explanation:** You can buy the stock on day 2 at price = 1 and sell it on day 5 at price = 9. Hence, the profit is 8.

**Input:** prices[] = [7, 6, 4, 3, 1]  
**Output:** 0 **Explanation****:** Here the prices are in decreasing order, hence if we buy any day then we cannot sell it at a greater price. Hence, the answer is 0.

**Input:** prices[] = [1, 3, 6, 9, 11]  
**Output:** 10   
**Explanation****:** Since the array is sorted in increasing order, we can make maximum profit by buying at price[0] and selling at price[n-1].

**Constraint:**  
1 <= prices.size()<= 105  
0 <= prices[i] <=104

---

### Minimize the Heights

Given an array **arr[]** denoting heights of **N** towers and a positive integer **K.**

For **each** tower, you must perform **exactly one** of the following operations **exactly once**.

- **Increase** the height of the tower by **K**
- **Decrease** the height of the tower by **K**

Find out the **minimum** possible difference between the height of the shortest and tallest towers after you have modified each tower.

You can find a slight modification of the problem [here](https://practice.geeksforgeeks.org/problems/minimize-the-heights-i/1/).  
**Note:** It is **compulsory** to increase or decrease the height by K for each tower. **After** the operation, the resultant array should **not** contain any **negative integers**.

**Examples :**

**Input:** k = 2, arr[] = {1, 5, 8, 10}
**Output:** 5
**Explanation:** The array can be modified as {1+k, 5-k, 8-k, 10-k} = {3, 3, 6, 8}.The difference between the largest and the smallest is 8-3 = 5.

**Input:** k = 3, arr[] = {3, 9, 12, 16, 20}
**Output:** 11
**Explanation:** The array can be modified as {3+k, 9+k, 12-k, 16-k, 20-k} -> {6, 12, 9, 13, 17}.The difference between the largest and the smallest is 17-6 = 11. 

**Expected Time Complexity:** O(n*logn)  
**Expected Auxiliary Space:** O(n)

---

### Kadane's Algorithm

Given an integer array **arr[].** You need to find the **maximum** sum of a subarray.  

**Examples:**

**Input:** arr[] = [2, 3, -8, 7, -1, 2, 3]
**Output:** 11
**Explanation:** The subarray {7, -1, 2, 3} has the largest sum 11.

**Input:** arr[] = [-2, -4]
**Output:** -2
**Explanation:** The subarray {-2} has the largest sum -2.

**Input:** arr[] = [5, 4, 1, 7, 8]
**Output:** 25
**Explanation:** The subarray {5, 4, 1, 7, 8} has the largest sum 25.

**Constraints:  
**1 ≤ arr.size() ≤ 105-109 ≤ arr[i] ≤ 104

---

### Maximum Product Subarray

Given an array **arr[]** that contains positive and negative integers (may contain 0 as well). Find the **maximum** product that we can get in a subarray of **arr[]**.

Note: It is guaranteed that the output fits in a 32-bit integer.

**Examples  
**

**Input:** arr[] = [-2, 6, -3, -10, 0, 2]
**Output:** 180
**Explanation:** The subarray with maximum product is {6, -3, -10} with product = 6 * (-3) * (-10) = 180.

**Input:** arr[] = [-1, -3, -10, 0, 6]
**Output:** 30
**Explanation:** The subarray with maximum product is {-3, -10} with product = (-3) * (-10) = 30.

**Input:** arr[] = [2, 3, 4]   
**Output:** 24   
**Explanation:** For an array with all positive elements, the result is product of all elements. 

**Constraints:**  
1 ≤ arr.size() ≤ 106  
-10  ≤  arr[i]  ≤  10

---

### Max Circular Subarray Sum

Given an array of integers **arr[]** in a **circular** fashion. Find the **maximum** subarray sum that we can get if we assume the array to be circular.

**Examples:**

**Input:** arr[] = [8, -8, 9, -9, 10, -11, 12]
**Output:** 22
**Explanation:** Starting from the last element of the array, i.e, 12, and moving in a circular fashion, we have max subarray as 12, 8, -8, 9, -9, 10, which gives maximum sum as 22.

**Input:** arr[] = [10, -3, -4, 7, 6, 5, -4, -1]
**Output:** 23
**Explanation:** Maximum sum of the circular subarray is 23. The subarray is [7, 6, 5, -4, -1, 10].  

**Input:** arr[] = [-1, 40, -14, 7, 6, 5, -4, -1]   
**Output:** 52
**Explanation:** Circular Subarray [7, 6, 5, -4, -1, -1, 40] has the maximum sum, which is 52.

**Constraints:**  
1 <= arr.size() <= 105  
-104 <= arr[i] <= 104

---

### Smallest Positive Mussing Number

You are given an integer array **arr**[]. Your task is to find the **smallest positive number** missing from the array.

Note: Positive number starts from 1. The array can have negative integers too.

**Examples:**

**Input:** arr[] = [2, -3, 4, 1, 1, 7]
**Output:** 3
**Explanation:** Smallest positive missing number is 3.

**Input:** arr[] = [5, 3, 2, 5, 1]
**Output:** 4
**Explanation:** Smallest positive missing number is 4.  

**Input:** arr[] = [-8, 0, -1, -4, -3]
**Output:** 1
**Explanation:** Smallest positive missing number is 1.

**Constraints:**    
1 <= arr.size() <= 105  
-106 <= arr[i] <= 106

---

