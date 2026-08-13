[[react hooks]] [[React State management]] [[React Architecture]] [[React pattern categorisation]] [[Component Presentational Pattern]] [[Composite pattern]]

# Provider pattern

> The provider model is a design pattern formulated by Microsoft for use in the ASP.NET Starter Kits and formalized in .NET version 2.0.

## What this is

The provider model is a design pattern formulated by Microsoft for use in the ASP.NET Starter Kits and formalized in .NET version 2.0. It is used to allow an application to choose from one of multiple implementations or "condiments" in the application configuration, for example, to provide access to different data stores to retrieve login information, or to use different storage methodologies such as a database, binary to disk, XML, etc.



React patterns are reusable composition strategies — how components share behavior without duplicating implementation. Modern code often prefers hooks and composition over legacy patterns, but recognizing each pattern helps when reading older codebases or choosing explicit component APIs.

## What breaks first

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Invalid hook call warning | Hook outside component or duplicate React copies | Call hooks only from components/custom hooks; dedupe `react` in bundle |
| Hydration mismatch | Server HTML differs from client render | Fix conditional rendering; avoid `Date.now()` in SSR output |
| State updates but UI stale | Mutation without setter | Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references |

## Recall

What breaks first in production if `Provider pattern` is misused — bundle size, stale UI, or hydration errors?

## Related

[[react hooks]] [[React State management]] [[React Architecture]] [[React pattern categorisation]] [[Component Presentational Pattern]] [[Composite pattern]]

## Sources

- [Wikipedia — Provider model](https://en.wikipedia.org/wiki/Provider_model)
