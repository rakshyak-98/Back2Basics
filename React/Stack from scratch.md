[[react hooks]] [[React State management]] [[React Architecture]] [[Separate functional logic from persentation components]]

# Stack from scratch

> Stack from scratch shapes how React applications compose UI, state, and side effects in production.

## What this is

Production React splits concerns across routing, feature modules, shared UI, client versus server state, and infrastructure (API clients, authentication, error boundaries). The first failure mode is usually duplicated server state in client stores or bundle bloat from importing server-only modules into client trees.

## What breaks first

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Invalid hook call warning | Hook outside component or duplicate React copies | Call hooks only from components/custom hooks; dedupe `react` in bundle |
| Hydration mismatch | Server HTML differs from client render | Fix conditional rendering; avoid `Date.now()` in SSR output |
| State updates but UI stale | Mutation without setter | Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references |

## Recall

What breaks first in production if `Stack from scratch` is misused — bundle size, stale UI, or hydration errors?

## Related

[[react hooks]] [[React State management]] [[React Architecture]] [[Separate functional logic from persentation components]]
