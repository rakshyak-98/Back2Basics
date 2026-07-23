[[javascript]] [[Operating System/abstract storage location]] [[Design pattern/Static Members]] [[compiler/library file]]

# Symbolic name

> Human-readable identifier bound to a program entity — variables, functions, constants — instead of raw literals — **readability + refactor safety**.

## Mental model

A **symbolic name** maps meaning to storage or behavior. The compiler/interpreter resolves the name to an address, register, or closure slot at compile or run time.

```
Source:     const MAX_RETRIES = 3;
                    │
Runtime:    name "MAX_RETRIES" → value 3 in binding

vs magic:   if (attempt > 3) …   // what is 3?
```

| Kind | Example | Why |
|------|---------|-----|
| **Constant** | `const RED = '#FF0000'` | Named color tokens |
| **Variable** | `let connectionCount = 0` | Mutable state |
| **Function** | `function parseInvoice()` | Named behavior |
| **Label** | `retry:` (assembly/Go) | Control flow target |

Same concept across languages: Python symbols, Rust bindings, DNS hostnames as symbolic network names.

## Standard config / commands

### Named constants (avoid magic values)

```javascript
const RED   = '#FF0000';
const GREEN = '#00FF00';
const BLUE  = '#0000FF';

function statusColor(ok) {
  return ok ? GREEN : RED;
}
```

### Enum-style (TypeScript)

```typescript
enum HttpStatus {
  Ok = 200,
  NotFound = 404,
}
```

### Configuration keys as symbols

```javascript
export const CONFIG_KEYS = {
  DB_URL: 'database.url',
  POOL_SIZE: 'database.poolSize',
} as const;
```

### Reverse lookup map

```javascript
const ROLE_BY_ID = { 1: 'admin', 2: 'user' };
const ID_BY_ROLE = Object.fromEntries(
  Object.entries(ROLE_BY_ID).map(([k, v]) => [v, Number(k)])
);
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong value, hard to trace | Magic number/string | Extract named constant |
| Rename broke runtime | Stringly-typed keys | Use constants or TS enums |
| Duplicate symbol names | Shadowing in nested scope | Rename or narrow block |
| Export name collision | Barrel re-exports | Explicit export aliases |
| Minified stack unreadable | Production build | Source maps; keep named fns in errors |

## Gotchas

> [!WARNING]
> **Symbolic names in logs/config must stay stable** — renaming env vars without migration breaks deploy scripts.

- **`const` object fields remain mutable** — name says constant binding, not deep freeze.
- **Dynamic keys** `obj[variable]` lose static rename support in IDEs.
- **DNS symbolic names** cache TTL — name resolution is not the same as JS binding lifetime.

## When NOT to use

- Ultra-local throwaway loop index `i` — noise if scope is 3 lines.
- Over-abstracting every literal (`const TWO = 2`) — hurts readability.

## Related

[[javascript]] [[Operating System/abstract storage location]] [[Design pattern/Static Members]] [[Descriptive/JavaScript/function]]
