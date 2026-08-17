[[react hooks]] [[React State management]] [[React Architecture]]

# re-export file

> Barrel `index.ts` that re-exports modules — shorter imports, but easy to create circular deps and fat bundles.

```txt
        re-export file ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about barrel files, tree-shaking, and circular import hazard…

## Sources
- [MDN — export](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export) — overview
- [Webpack tree shaking](https://webpack.js.org/guides/tree-shaking/) — deep-dive

## Key Concepts
- **Convenience:** `import { Button } from '@/ui'`.
- **Cost:** accidental pull of heavy modules; cycles through index.
- **Mitigation:** path imports for heavy leaves; avoid side effects in barrels.


- **Core:** A re-export (barrel) file aggregates `export * from` / named exports so consu…

## Technical Details
```ts
// ui/index.ts
export { Button } from './Button'
export { Modal } from './Modal'
```

## Mistakes to Avoid
- **Mistake:** Barrel that re-exports a whole app folder
- **Circular `A::** → index → B → index → A`

## Pros/Cons or Trade-offs
- **Pro:** Stable public API surface.
- **Con:** Can defeat tree-shaking and hide dependency cycles.

## Comparison
- vs deep imports: more verbose but clearer bundle boundaries.


### Use cases
- Design-system package exposes a clean public API via barrels while keeping in…
