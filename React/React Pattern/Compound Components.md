[[react hooks]] [[React State management]] [[React Architecture]] [[Compound Components 1]] [[React pattern categorisation]] [[Separate functional logic from persentation components]]

# Compound Components

> Compound Components shapes how React applications compose UI, state, and side effects in production.

## What this is

React patterns are reusable composition strategies — how components share behavior without duplicating implementation. Modern code often prefers hooks and composition over legacy patterns, but recognizing each pattern helps when reading older codebases or choosing explicit component APIs.

## What breaks first

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Invalid hook call warning | Hook outside component or duplicate React copies | Call hooks only from components/custom hooks; dedupe `react` in bundle |
| Hydration mismatch | Server HTML differs from client render | Fix conditional rendering; avoid `Date.now()` in SSR output |
| State updates but UI stale | Mutation without setter | Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references |

## Recall

What breaks first in production if `Compound Components` is misused — bundle size, stale UI, or hydration errors?

## Related

[[react hooks]] [[React State management]] [[React Architecture]] [[Compound Components 1]] [[React pattern categorisation]] [[Separate functional logic from persentation components]]
