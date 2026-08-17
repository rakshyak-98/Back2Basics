[[JavaScript]] [[Data access patterns]] [[Epoll]] [[Progressive search functionality]] [[Animation]] [[webSocket]]

# Frontend Datastructure

> Maps, sets, rings, and queues FE engineers use daily for UI state, caches, and render performance — not CLRS trivia.

```txt
        Frontend Datastruc ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Frontend structure choices (Map/Set/ring buffers) show up in UI performance i…

## Sources
- [MDN — Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) — overview
- [MDN — Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) — overview

## Key Concepts
- **Note:** Browser JS gives you **Map/Set** (O(1) avg keyed operations), **Array** (orde…

```txt
UI pattern              → Structure
─────────────────────────────────────
Id → entity lookup      → Map<id, Entity>
Dedupe selections       → Set<id>
LRU / bounded cache     → Map + doubly-linked OR ring buffer
Undo stack              → Array (stack)
FIFO work queue         → Array deque or ring buffer
Priority updates        → Map + sorted index (or heap lib)
```

- **Note:** **React note:** immutable updates

- **Note:** **Big-O in FE matters when:** virtual lists (10k+ rows), graph editors, real-…

## Technical Details
### Map vs Object

```javascript
// ✅ Map: any key type, size, iteration order, no prototype pollution
const byId = new Map();
byId.set(item.id, item);
byId.get(id);
byId.delete(id);

// Object OK for fixed string keys / JSON serialization
const flags = { darkMode: true };
```

### Set for membership

```javascript
const selected = new Set();
selected.add(id);
selected.has(id);       // O(1)
[...selected];          // render checklist
```

### Ring buffer (fixed-size time series / logs)

```javascript
class RingBuffer {
  constructor(capacity) {
    this.buf = new Array(capacity);
    this.cap = capacity;
    this.i = 0;
    this.len = 0;
  }
  push(v) {
    this.buf[this.i] = v;
    this.i = (this.i + 1) % this.cap;
    this.len = Math.min(this.len + 1, this.cap);
  }
  toArray() {
    const start = this.len < this.cap ? 0 : this.i;
    return Array.from({ length: this.len }, (_, k) =>
      this.buf[(start + k) % this.cap]
    );
  }
}
```

### LRU cache (Map insertion order trick)

```javascript
class LRU {
  constructor(limit) { this.limit = limit; this.map = new Map(); }
  get(k) {
    if (!this.map.has(k)) return undefined;
    const v = this.map.get(k);
    this.map.delete(k);
    this.map.set(k, v); // refresh MRU
    return v;
  }
  set(k, v) {
    if (this.map.has(k)) this.map.delete(k);
    this.map.set(k, v);
    if (this.map.size > this.limit) {
      const first = this.map.keys().next().value;
      this.map.delete(first);
    }
  }
}
```

### Index by multiple keys (inverted index)

```javascript
// tag → Set of item ids (faceted filter UI)
const byTag = new Map();
for (const item of items) {
  for (const tag of item.tags) {
    if (!byTag.has(tag)) byTag.set(tag, new Set());
    byTag.get(tag).add(item.id);
  }
}
```

### WeakMap for component metadata

```javascript
const meta = new WeakMap(); // keys are objects; no memory leak when DOM node gone
meta.set(domNode, { lastMeasure: 42 });
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| UI lag typing in big list | O(n) filter each keystroke | Pre-index; debounce; [[Progressive search functionality]] |
| Memory grows unbounded | Global cache Map | LRU cap; WeakMap for DOM-bound data |
| Stale UI after update | Mutated Map in place | New Map reference for React memo |
| Wrong render order | Object key sort | Map preserves insertion; explicit sort key |
| Duplicate keys in virtual list | Index as React key | Stable entity id from Map |
| Race in async fetch | Last-write-wins | Request id / AbortController + Map stamp |

## Mistakes to Avoid
- **Mistake:** `Object` keys are strings
- **Mistake:** Spread huge Set/Map every render
- **`JSON.stringify(Map)`::** → `{}` — serialize to entries array for persistence
- **Mistake:** Sorted array + splice for queue

## Pros/Cons or Trade-offs
- **Trade-off:** < 100 items — plain array + `find` is fine; don't pre-optimize.
- **Trade-off:** Server-authoritative pagination — client Map of "all rows" fights product; page cache only.
- **Trade-off:** Replace DB index — client structures mirror UX needs, not SQL semantics.
