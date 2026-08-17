[[Descriptive/JavaScript/execution context]] [[Descriptive/JavaScript/constructor function]] [[javascript]] [[NodeJS/Event Loop]] [[Descriptive/JavaScript/Concurrency]]

# Function (JavaScript)

> First-class callable object — closures, `this`, and properties on the function itself — **ECMAScript + daily API design**.

```txt
        Function (JavaScri ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Function interviews cover declarations vs expressions, closures, and first-cl…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** Functions are values: assign, pass, return, store on objects. Each **invocati…

```
const fn = function add(a, b) { return a + b; };
- **Note:** fn.customMeta = { version: 1 }; // legal — functions are objects

fn(2, 3) → new context → return 5 → context popped
```

| Form | `this` | Hoisting |
|------|--------|----------|
| Function declaration | call-site | whole block |
| Function expression | call-site | name only inside expr |
| Arrow function | lexical `this` | not hoisted as fn |
| Method shorthand | receiver object | like declaration |

## Technical Details
### Core patterns

```javascript
// Declaration
function parseConfig(raw) { return JSON.parse(raw); }

// Expression + named for stack traces
const parse = function parseConfig(raw) { … };

// Arrow — no own this/arguments
const ids = users.map(u => u.id);

// Rest / default
function connect(host, port = 443, ...opts) { … }
```

### `flatMap` — map then flatten one level

```javascript
const arr = [1, 2, 3];

const mapped = arr.map(x => [x, x * 2]);
// [[1, 2], [2, 4], [3, 6]] — nested

const flatMapped = arr.flatMap(x => [x, x * 2]);
// [1, 2, 2, 4, 3, 6] — one level flat
```

- Use `flatMap` when mapper returns arrays and you want a single list

### Custom properties on functions (metadata, caches)

```javascript
function api(route) {
  if (!api.cache) api.cache = new Map();
  …
}
api.cache = new Map(); // clearer than implicit create-on-first-call
```

### Higher-order / curry

```javascript
const withAuth = (token) => (req) => fetch(req, {
  headers: { Authorization: `Bearer ${token}` },
});
```

## Mistakes to Avoid
> [!WARNING]
> Functions are **mutable objects** — reassigning `parseConfig = null` does not remove it from closures that already captured the old reference.

- **Mistake:** **`function.length`:** count of parameters before first default/…
- **Mistake:** **Generator/async:** return iterators/promises
- **Mistake:** **Strict mode** in modules and classes

| Symptom | Check | Fix |
|---------|-------|-----|
| `fn is not a function` | Import/export mismatch | Default vs named export |
| Wrong arity silently | Extra args ignored | Validate length or use TS |
| `this` undefined in method passed as callback | Detached method | `bind`, arrow wrapper, or class field |
| Stack overflow | Recursion | Iterate or trampoline |
| Memory growth | Closure over big scope | Narrow captured vars |

## Pros/Cons or Trade-offs
- One-liner used once — inline or extract only when name clarifies intent.
- Class when only data — plain object or record type may suffice.
