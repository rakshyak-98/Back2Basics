[[React]] [[react-query]] [[Redux/Redux createApi]] [[Optimizing performance]]

# react cache / TanStack Query cache

> Client in-memory cache of server responses — update it after mutations so UI stays in sync without a full refetch.





## Interview Relevance
Interviewers want concrete re-render causes and fixes (memoization, keys, list virtualization) — not vague “optimize React.”

## Sources
- [Wikipedia — react cache](https://en.wikipedia.org/wiki/react_cache) — overview

## Key Concepts
- **queryKey:** Cache address for this data — “Same key = shared cache across components.”
- **invalidate:** Mark stale, refetch — “After create, invalidate the list.”
- **Optimistic update:** Patch UI before server replies — “Roll back if the request fails.”

## Technical Details
```txt
queryKey → QueryCache (RAM)
mutation ──► onSuccess: setQueryData | invalidateQueries
failure  ──► rollback optimistic patch
```

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

## Real-World Applications
Apply react cache / TanStack Query cache in feature code where the Key Concepts match; verify with the Mistakes table.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Client-only UI state** — `useState` / Zustand, not Query cache.
- **Con / skip when:** **authentication secrets** — don’t persist sensitive query data to `localStorage`.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| UI stale after mutate | Didn’t update/invalidate key | `setQueryData` or invalidate correct key |
| Flicker then wrong data | Optimistic shape ≠ server | Align types; always settle with invalidate |
| Cache empty after F5 | In-memory only | Persist plugin or accept refetch |
| Duplicate fetches | Different queryKeys | Normalize keys (stable serialization) |

- **Hard refresh clears RAM cache** — not Redis, not backend. Soft reload often keeps it.
- **Wrong key = silent miss** — `['todo', 1]` vs `['todos', 1]` never sync.
