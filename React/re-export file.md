[[React]] [[node modules]]

# re-export file (barrel)

> One `index.ts` that re-exports a folder’s public API — shorter imports, clear package surface.

---

## Mental model

**Say it in one breath:** Consumers import from `@/api/hotels` instead of deep paths; the barrel lists what is public.

```txt
hotels/
  getHotels.ts
  types.ts
  index.ts  ← export { getHotels } from './getHotels'
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Barrel** | Folder `index` re-exports | “Public API for the module.” |
| **Explicit export** | `export { x } from './x'` | “Safer than `export *` for packages.” |
| **Tree-shaking** | Bundler drops unused exports | “Wildcards can defeat shaking in some setups.” |

## Standard config / commands

```ts
// src/api/hotels/index.ts
export { getHotels } from './getHotels'
export { getHotelById } from './getHotelById'
export * from './types'
export { hotelKeys } from './constants'
```

```ts
import { getHotels, hotelKeys } from '@/api/hotels'
```

| Knob | Why it matters |
|------|----------------|
| Explicit named re-exports | Avoid name clashes; clearer graph |
| `export *` for types | Usually OK for type-only modules |
| Published npm `index` | Prefer explicit exports only |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Circular dependency | A→index→B→index→A | Import concrete files inside the folder |
| Bundle includes unused code | `export *` / side-effect imports | Explicit exports; check bundler |
| Name collision | Two modules export same name | Alias on re-export |
| Slow TS / IDE | Huge mega-barrels | Split by domain; fewer deep barrels |

---

## Gotchas

> [!WARNING]
> **`export *` in a published package** — accidental API surface and shaky tree-shaking. Be explicit.

> [!WARNING]
> **Barrels ↔ cycles** — internal files should import siblings directly, not via their own barrel.

---

## When NOT to use

- **One-file folders** — no barrel needed.
- **Hot paths where cycles appear** — direct imports win.

---

## Related

[[Typescript with react]] [[React code smells]]
