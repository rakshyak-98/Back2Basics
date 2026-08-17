[[Data structure/dsa genera formula]] [[Data structure/algo/binary search]] [[Operating System/Stack Frame]]

# Linked list

> Linked list — don't use linked list for cache-friendly bulk storage — arrays win CPU cache.





## Interview Relevance
Linked lists test pointer/reference reasoning — reverse, cycle detect, and when arrays beat lists on modern CPUs.

## Sources
- [Wikipedia — Linked list](https://en.wikipedia.org/wiki/Linked_list) — overview
- [CLRS — Linked lists](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) — deep-dive

## Key Concepts
Each node holds **value** + **next** pointer. Head is entry; tail optional for O(1) append with doubly-linked + tail reference. Singly-linked: one direction. Doubly-linked: `prev` enables backward walk and O(1) delete given node reference. No random access — index i requires i steps from head.

```
head → [1|•]→[2|•]→[3|null]
       doubly: [1|•↔•]⇄[2|•↔•]⇄[3|null←•]
```

## Technical Details
### Singly-linked (JS)

```js
class Node {
  constructor(val, next = null) { this.val = val; this.next = next; }
}

function prepend(head, val) {
  return new Node(val, head);
}

function insertAfter(node, val) {
  node.next = new Node(val, node.next);
}
```

### Dummy head (simplifies delete)

```js
function removeVal(head, val) {
  const dummy = new Node(0, head);
  let cur = dummy;
  while (cur.next) {
    if (cur.next.val === val) cur.next = cur.next.next;
    else cur = cur.next;
  }
  return dummy.next;
}
```

### Fast/slow pointer (cycle, middle)

```js
let slow = head, fast = head;
while (fast?.next) {
  slow = slow.next;
  fast = fast.next.next;
}
// slow at middle; cycle detection if fast meets slow
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Lost rest of list | Assignment order | `node.next = node.next.next` save refs first |
| Infinite loop | Cycle | Floyd cycle detection |
| Off-by-one tail | Empty list | Dummy head; check `head === null` |
| Memory leak (C/C++) | Free on delete | `free(node)` when removing |
| Reverse bugs | 3-pointer walk | `prev, cur, next` pattern |

## Pros/Cons or Trade-offs
- **Trade-off:** Don't use linked list for cache-friendly bulk storage — arrays win CPU cache.
- **Trade-off:** Don't choose LL for frequent binary search — array + BS instead.

## Mistakes to Avoid
- Mutating while iterating — save `next` before deleting current. Shared node in two lists — aliasing unless deep copy. Interview "reverse in k-group" — pointer discipline; draw diagram.
