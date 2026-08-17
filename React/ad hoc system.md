[[react hooks]] [[React State management]] [[React Architecture]] [[Data Fetching HOC component]]

# ad hoc system

> One-off state and fetch wiring scattered across components — works in a spike, fights you in production.

```txt
        ad hoc system ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers contrast disciplined data/state boundaries with ad-hoc effects a…

## Sources
- [React — Thinking in React](https://react.dev/learn/thinking-in-react) — overview
- [React — Managing State](https://react.dev/learn/managing-state) — deep-dive

## Key Concepts
- **Local invention:** Every screen has its own `useEffect` fetch + loading flag.
- **No shared client:** Headers, base URL, and error mapping copied per file.
- **Prop drilling / random Context:** Cross-cutting state appears without a clear owner.


- **Core:** An ad hoc React system means each feature invents its own fetch, cache, and e…

## Technical Details
- Smell checklist:

| Smell | Prefer instead |
|-------|----------------|
| `useEffect` + `fetch` in 10 screens | [[react-query]] |
| Modal + user + cart all in one Context | Split stores / [[zustand]] slices |
| Copy-pasted loading spinners | Shared Suspense / query status UI |

## Mistakes to Avoid
- **Mistake:** Calling a working spike “done” without extracting the API/query …
- **Mistake:** Adding Redux “for structure” while still fetching ad hoc in comp…

## Pros/Cons or Trade-offs
- **Pro:** Fast for prototypes and throwaway demos.
- **Con:** Race conditions, duplicate requests, and inconsistent error UX at team scale.

## Comparison
- vs [[React Architecture]]: architecture names owners and boundaries


### Use cases
- MVP ships with fetch-in-effect everywhere
