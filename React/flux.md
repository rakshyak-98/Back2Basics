[[react hooks]] [[React State management]] [[React Architecture]]

# flux

> Flux describes any effect that appears to pass or travel through a surface or substance.

## What this is

Flux describes any effect that appears to pass or travel through a surface or substance. Flux is a concept in applied mathematics and vector calculus which has many applications in physics. For transport phenomena, flux is a vector quantity, describing the magnitude and direction of the flow of a substance or property. In vector calculus, flux is a scalar quantity, defined as the surface integral of the perpendicular component of a vector field over a surface.



Production React splits concerns across routing, feature modules, shared UI, client versus server state, and infrastructure (API clients, authentication, error boundaries). The first failure mode is usually duplicated server state in client stores or bundle bloat from importing server-only modules into client trees.

## What breaks first

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Invalid hook call warning | Hook outside component or duplicate React copies | Call hooks only from components/custom hooks; dedupe `react` in bundle |
| Hydration mismatch | Server HTML differs from client render | Fix conditional rendering; avoid `Date.now()` in SSR output |
| State updates but UI stale | Mutation without setter | Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references |

## Recall

What breaks first in production if `flux` is misused — bundle size, stale UI, or hydration errors?

## Related

[[react hooks]] [[React State management]] [[React Architecture]]

## Sources

- [Facebook Flux — GitHub](https://github.com/facebookarchive/flux)
- [Wikipedia — Flux](https://en.wikipedia.org/wiki/Flux)
