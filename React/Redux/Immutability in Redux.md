[[Redux]] [[Packages/Immer]] [[Redux toolkit]]

# Immutability in Redux

> Never mutate the state tree in place — return new objects/arrays so React-Redux can detect changes by reference.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Copy every nested level you change. RTK uses Immer so you *write* mutating syntax while it produces immutable updates.

```txt
state.user.name = 'Ada'          // ❌ outside Immer
return { ...state, user: { ...state.user, name: 'Ada' } }  // ✅
// RTK createSlice: OK to "mutate" draft
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Immutable update** | New reference for changed path | “Shallow copy each nesting level.” |
| **Immer draft** | Proxy you can “mutate” | “RTK reducers use drafts under the hood.” |
| **Structural sharing** | Unchanged branches keep refs | “Selectors skip work when ref equal.” |

## Standard config / commands

```ts
// Hand-written
return { ...state, items: state.items.map((i) => (i.id === id ? { ...i, done: true } : i)) }

// RTK + Immer
createSlice({
  name: 'todos',
  initialState: { items: [] as Todo[] },
  reducers: {
    toggle(state, action: PayloadAction<string>) {
      const t = state.items.find((i) => i.id === action.payload)
      if (t) t.done = !t.done // draft mutation OK
    },
  },
})
```

| Knob | Why it matters |
|------|----------------|
| Spread nesting | Miss a level → accidental shared mutation |
| `immutableCheck` middleware | Catches mutations in dev |
| Don’t return draft *and* mutate oddly | Prefer mutate draft *or* return new state |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| UI doesn’t update | Mutated in place | Copy path / use RTK slice |
| Dev “invariant failed” mutation | Something wrote to state | Find write outside reducer |
| Nested field update lost | Spread only top level | Copy each nesting level |
| Huge spreads painful | Deep trees | Normalize state; use Immer |

---

## Gotchas

> [!WARNING]
> **Mutating outside reducers** (in components) breaks time-travel and subscriptions.

> [!WARNING]
> **Arrays: `push` on real state** — only safe on Immer drafts inside `createSlice`.

---

## When NOT to use

- **Local component state** — normal `useState` replace is enough; no Redux immutability ceremony.
- **Hand-rolling deep copies everywhere** — use RTK/Immer instead.

---

## Related

[[Redux toolkit]] [[Redux/Redux createSlice]] [[Packages/Immer]]
