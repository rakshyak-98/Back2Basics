### 1. **Bubble Sort**
```javascript
function bubbleSort(arr) {
  const n = arr.length;
  for (let i = 0; i < n - 1; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]]; // Swap elements
      }
    }
  }
  return arr;
}

console.log(bubbleSort([...largeArray]));
```

**Time Complexity:** O(n²)  
**Example Output:** `[2, 3, 6, 7, 9, 12, 15, 24, 27, ...]`

### 2. **Selection Sort**
```javascript
function selectionSort(arr) {
  const n = arr.length;
  for (let i = 0; i < n - 1; i++) {
    let minIndex = i;
    for (let j = i + 1; j < n; j++) {
      if (arr[j] < arr[minIndex]) {
        minIndex = j;
      }
    }
    [arr[i], arr[minIndex]] = [arr[minIndex], arr[i]]; // Swap
  }
  return arr;
}

console.log(selectionSort([...largeArray]));
```

**Time Complexity:** O(n²)  
**Example Output:** `[2, 3, 6, 7, 9, 12, 15, 24, 27, ...]`

### 3. **Insertion Sort**
```javascript
function insertionSort(arr) {
  const n = arr.length;
  for (let i = 1; i < n; i++) {
    let key = arr[i];
    let j = i - 1;
    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      j--;
    }
    arr[j + 1] = key;
  }
  return arr;
}

console.log(insertionSort([...largeArray]));
```

**Time Complexity:** O(n²)  
**Example Output:** `[2, 3, 6, 7, 9, 12, 15, 24, 27, ...]`

### 4. **Merge Sort**
```javascript
function mergeSort(arr) {
  if (arr.length <= 1) return arr;

  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));

  return merge(left, right);
}

function merge(left, right) {
  const result = [];
  while (left.length && right.length) {
    if (left[0] < right[0]) result.push(left.shift());
    else result.push(right.shift());
  }
  return result.concat(left, right);
}

console.log(mergeSort([...largeArray]));
```

**Time Complexity:** O(n log n)  
**Example Output:** `[2, 3, 6, 7, 9, 12, 15, 24, 27, ...]`

### 5. **Quick Sort**
```javascript
function quickSort(arr) {
  if (arr.length <= 1) return arr;

  const pivot = arr[arr.length - 1];
  const left = [];
  const right = [];

  for (let i = 0; i < arr.length - 1; i++) {
    if (arr[i] < pivot) left.push(arr[i]);
    else right.push(arr[i]);
  }

  return [...quickSort(left), pivot, ...quickSort(right)];
}

console.log(quickSort([...largeArray]));
```

**Time Complexity:**  
- **Average Case:** O(n log n)  
- **Worst Case:** O(n²) (for already sorted arrays)

**Example Output:** `[2, 3, 6, 7, 9, 12, 15, 24, 27, ...]`

### 6. **JavaScript Built-in Sort**
```javascript
const sortedArray = [...largeArray].sort((a, b) => a - b);
console.log(sortedArray);
```

**Time Complexity:** O(n log n)  
**Example Output:** `[2, 3, 6, 7, 9, 12, 15, 24, 27, ...]`

---

### Summary Table

| Algorithm      | Time Complexity (Average) | Code Complexity | Suitable For       |
| -------------- | ------------------------- | --------------- | ------------------ |
| Bubble Sort    | O(n²)                     | Simple          | Small arrays       |
| Selection Sort | O(n²)                     | Simple          | Small arrays       |
| Insertion Sort | O(n²)                     | Simple          | Nearly sorted data |
| Merge Sort     | O(n log n)                | Moderate        | General use        |
| Quick Sort     | O(n log n)                | Moderate        | General use        |
| Built-in Sort  | O(n log n)                | Easy            | General use        |

Let me know if you want further details or examples for a specific sorting algorithm.