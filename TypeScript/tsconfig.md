<!-- note-strategy: operational -->
[[TypeScript]] [[typescript]] [[typescript types]]

# tsconfig

> `tsconfig.json` — compiler project file: roots, `strict` flags, module settings, path aliases, incremental build info.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** One configuration (or solution-style references) tells `tsc` what to include and how strict to be. Bundlers may typecheck separately — keep options aligned.

```txt
include/exclude → parse → typecheck → emit?
```

| Area | Knobs |
|------|-------|
| Safety | `strict`, `noUncheckedIndexedAccess` |
| Modules | `module`, `moduleResolution`, `verbatimModuleSyntax` |
| Output | `outDir`, `declaration`, `noEmit` |
| DX | `paths`, `baseUrl`, `incremental` |

---

## Standard config / commands

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true,
    "types": ["node"],
    "tsBuildInfoFile": ".cache/tsbuildinfo"
  },
  "include": ["src"]
}
```

```bash
npx tsc -p tsconfig.json --noEmit
npx tsc -b  # project references
```

| Knob | Why it matters |
|------|----------------|
| `typeRoots` / `types` | Which `@types` load |
| `paths` | Aliases — bundler must mirror |
| `incremental` + `tsBuildInfoFile` | Faster rebuilds |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t find `@types` | `types`/`typeRoots` too narrow | Remove empty `types: []` or add names |
| Path alias fails at runtime | Only TS knows paths | Bundler/`subpath` exports |
| IDE ≠ CLI errors | Wrong tsconfig root | Point VS Code at right config |
| Slow CI | No incremental cache | Cache `tsbuildinfo` |
| Emit into repo mess | Accidental emit | `noEmit` or clean `outDir` |

---

## Gotchas

> [!WARNING]
> **`paths` is not Node resolution** — runtime needs real resolution.

> [!WARNING]
> **`skipLibCheck`** — speeds CI; hides some `.d.ts` issues.

> [!WARNING]
> **Multiple tsconfigs** — app vs node vs test; don’t mix casually.

---

## When NOT to use

- **One-off `tsc` file** — `--allowJs` script maybe.
- **Fighting the bundler** — let Vite/webpack own emit; use `noEmit`.
- **Loosening `strict` to silence** — fix types.

---

## Related

[[typescript]] [[typescript error]] [[ambient modules]] [[Triple-Slash Directives]]
