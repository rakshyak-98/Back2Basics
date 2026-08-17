[[JavaScript]] [[Animation]] [[Frontend Datastructure]] [[webSocket]] [[redis-cli]] [[covering index]]

# Progressive search functionality

> Progressive search functionality — keystroke → debounce window → abort prior fetch → new query → render results

```txt
        Progressive search ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Progressive search interviews cover debounce, ranking, and accessibility of l…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
- **Note:** Keystroke → debounce window → abort prior fetch → new query → render results
                ↑                      ↑
           drop noise            race-safe UI
```

- **Note:** **Progressive search** = results refine as user types (autocomplete, catalog …

**Three costs:**
- **Note:** 1. **Network** — one request per term without debounce → DDoS your own API
2. **Server** — `%term%` LIKE without index → DB CPU spike
- **Note:** 3. **Client**

## Technical Details
### Debounced fetch with abort

```javascript
let timer;
let controller;

function onInput(query) {
  clearTimeout(timer);
  controller?.abort();

  if (!query.trim()) {
    setResults([]);
    return;
  }

  timer = setTimeout(async () => {
    controller = new AbortController();
    setLoading(true);
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`, {
        signal: controller.signal,
      });
      const data = await res.json();
      setResults(data.items);
    } catch (e) {
      if (e.name !== 'AbortError') setError(e);
    } finally {
      setLoading(false);
    }
  }, 250); // 200–350ms typical; shorter for local index
}
```

### React hook sketch

```javascript
function useDebouncedValue(value, ms = 300) {
  const [v, setV] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setV(value), ms);
    return () => clearTimeout(t);
  }, [value, ms]);
  return v;
}
// useDebouncedValue(input) → triggers SWR/React Query key
```

### Client-side index (small catalog)

```javascript
// Build once — [[Frontend Datastructure]] inverted index
const index = buildPrefixIndex(items, item => item.name.toLowerCase());

function searchLocal(q) {
  const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
  return terms.reduce((acc, t) => intersect(acc, index.get(t) ?? []), allIds);
}
```

### Server patterns

```sql
-- Postgres: prefix search — requires index strategy
-- pg_trgm for fuzzy; tsvector for full-text
CREATE INDEX idx_products_name_trgm ON products USING gin (name gin_trgm_ops);
```

```txt
API: GET /search?q=foo&limit=20
     Cache-Control: private, max-age=0 (usually)
     Rate limit per IP/session
     Return highlight snippets + stable id
```

### UX essentials

```txt
- Min chars before search (2–3) unless local index
- Keyboard: ↑↓ navigate, Enter select, Esc clear
- Announce loading/empty for a11y (aria-live polite)
- Preserve query in URL ?q= for share/back
```

## Mistakes to Avoid
> [!WARNING]
> **Debounce ≠ throttle** — throttle fires on interval (scroll); search wants debounce (quiet period).

> [!WARNING]
> **Leading wildcard LIKE `%foo`** — index unusable; require prefix or full-text.

> [!WARNING]
> **Logging raw queries** — PII in search strings; redact in analytics.

> [!WARNING]
> **SSR search** — don't hydrate mismatch; defer client fetch or match server results.

| Symptom | Check | Fix |
|---------|-------|-----|
| DB CPU spike on typing | Query plan / missing index | Trigram/FTS index; debounce; min length |
| Stale results flash | Race (slow response wins) | AbortController; request sequence id |
| Feels laggy | Time to first paint | Optimistic skeleton; local prefix index |
| Mobile keyboard jank | Input handler work | Debounce; virtualize list |
| Empty for valid terms | Encoding / case | `encodeURIComponent`; normalize Unicode NFC |
| Rate limit 429 | Aggressive polling | ↑ debounce; server-side coalesce |

## Pros/Cons or Trade-offs
- **Small fixed dropdown (< 20 items)**
- **Heavy analytics query** — batch/report UI, not per-keystroke.
- **Offline-first with tiny dataset** — filter in memory; skip network entirely.
