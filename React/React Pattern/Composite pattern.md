[[react hooks]] [[React State management]] [[React Architecture]] [[React pattern categorisation]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]]

# Composite pattern

> In software engineering, the composite pattern is a partitioning design pattern.

## What this is

In software engineering, the composite pattern is a partitioning design pattern. The composite pattern describes a group of objects that are treated the same way as a single instance of the same type of object. The intent of a composite is to "compose" objects into tree structures to represent part-whole hierarchies. Implementing the composite pattern lets clients treat individual objects and compositions uniformly.



React patterns are reusable composition strategies — how components share behavior without duplicating implementation. Modern code often prefers hooks and composition over legacy patterns, but recognizing each pattern helps when reading older codebases or choosing explicit component APIs.

## What breaks first

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Invalid hook call warning | Hook outside component or duplicate React copies | Call hooks only from components/custom hooks; dedupe `react` in bundle |
| Hydration mismatch | Server HTML differs from client render | Fix conditional rendering; avoid `Date.now()` in SSR output |
| State updates but UI stale | Mutation without setter | Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references |

## Recall

What breaks first in production if `Composite pattern` is misused — bundle size, stale UI, or hydration errors?

## Related

[[react hooks]] [[React State management]] [[React Architecture]] [[React pattern categorisation]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]]

## Sources

- [Wikipedia — Composite pattern](https://en.wikipedia.org/wiki/Composite_pattern)
