```text
[baseline-browser-mapping] The data in this module is over two months old.  To ensure accurate Baseline data, please update: `npm i baseline-browser-mapping@latest -D`
```
- `baseline-browser-mapping` -> This package maintains a mapping of browser versions that support features in the Web Platform Baseline.

---

```text
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
```

```bash
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

Because **Node.js intentionally limits the amount of memory (heap) a JavaScript process can use**.

Without a limit, a buggy application could consume all available RAM and make the entire system unstable.

### What happens internally

```text
npm run build
       ↓
npm starts Node.js
       ↓
Node starts V8 (JavaScript engine)
       ↓
V8 allocates a heap with a maximum size
       ↓
Your application stores objects in the heap
       ↓
Heap becomes full
       ↓
Garbage Collector tries to free memory
       ↓
Still insufficient memory
       ↓
"JavaScript heap out of memory"
```

---

### Why increase `--max-old-space-size`?

Some operations legitimately need lots of memory:
- Large frontend builds (`vite`, `webpack`, `next build`)
- TypeScript compilation
- Large monorepos
- Processing huge JSON/CSV files
- Generating source maps
- Static site generation

Default limits may be too small for these workloads.

Example:

```text
100 files     → OK
10,000 files  → More memory required
```

---

### Why not make it unlimited by default?

Tradeoffs:
- One process could consume all RAM.
- The OS may start using swap heavily.
- Other applications become slow.
- The system may become unresponsive.
- Memory leaks would be harder to detect.

The limit acts as a safety boundary.

---

### `--max-old-space-size` specifically

V8 divides memory into generations.

```text
Heap
├── Young generation
└── Old generation
```

`--max-old-space-size=4096`

means:
> Allow the **old generation** to grow up to **4096 MB (4 GB)**.
> Most long-lived objects eventually end up here.

---

### Important

Increasing memory is often a **symptom workaround**, not always the real fix.

If your build suddenly requires much more memory than before, investigate:
- Memory leaks
- Huge dependencies
- Large assets
- Inefficient build configuration
- Infinite object creation

Use more memory **only when the workload genuinely requires it**.