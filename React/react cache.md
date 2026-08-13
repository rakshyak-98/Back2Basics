[[React]] [[react-query]]

# react cache / TanStack Query cache

> Client in-memory cache of server responses — update it after mutations so UI stays in sync without a full refetch.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Mutation succeeds → patch the cached query (or invalidate) so every subscriber re-renders with fresh data.

```txt
queryKey → QueryCache (RAM)
mutation ──► onSuccess: setQueryData | invalidateQueries
failure  ──► rollback optimistic patch
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **queryKey** | Cache address for this data | “Same key = shared cache across components.” |
| **invalidate** | Mark stale, refetch | “After create, invalidate the list.” |
| **Optimistic update** | Patch UI before server replies | “Roll back if the request fails.” |

## Standard config / commands

```ts
useMutation({
  mutationFn: updateTodo,
  onMutate: async (todo) => {
    await qc.cancelQueries({ queryKey: ['todo', todo.id] })
    const prev = qc.getQueryData(['todo', todo.id])
    qc.setQueryData(['todo', todo.id], todo)
    return { prev }
  },
  onError: (_e, todo, ctx) => qc.setQueryData(['todo', todo.id], ctx?.prev),
  onSettled: (_d, _e, todo) => qc.invalidateQueries({ queryKey: ['todo', todo.id] }),
})
```

| Knob | Why it matters |
|------|----------------|
| `setQueryData` | Instant UI when response shape matches |
| `invalidateQueries` | Safe when many lists touch the resource |
| Optimistic + rollback | Snappy UX; must restore on error |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| UI stale after mutate | Didn’t update/invalidate key | `setQueryData` or invalidate correct key |
| Flicker then wrong data | Optimistic shape ≠ server | Align types; always settle with invalidate |
| Cache empty after F5 | In-memory only | Persist plugin or accept refetch |
| Duplicate fetches | Different queryKeys | Normalize keys (stable serialization) |

---

## Gotchas

> [!WARNING]
> **Hard refresh clears RAM cache** — not Redis, not backend. Soft reload often keeps it.

> [!WARNING]
> **Wrong key = silent miss** — `['todo', 1]` vs `['todos', 1]` never sync.

---

## When NOT to use

- **Client-only UI state** — `useState` / Zustand, not Query cache.
- **authentication secrets** — don’t persist sensitive query data to `localStorage`.

---

## Related

[[react-query]] [[Redux/Redux createApi]] [[Optimizing performance]]
