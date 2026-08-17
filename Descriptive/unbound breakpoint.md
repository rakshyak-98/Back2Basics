[[Descriptive/vscode]] [[javascript]] [[NodeJS/node command]] [[compiler/library file]] [[Descriptive/JavaScript/execution context]]

# Unbound breakpoint

> Unbound breakpoint — a breakpoint is bound when the debugger links it to an exact script location (file URL + line → bytecode offset). Unbound means

```txt
        Unbound breakpoint ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Unbound breakpoint questions diagnose source-map/path mismatches

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Technical Details
### VS Code — verify launch config

```json
{
  "type": "node",
  "request": "launch",
  "program": "${workspaceFolder}/src/index.ts",
  "runtimeArgs": ["-r", "ts-node/register"],
  "sourceMaps": true,
  "outFiles": ["${workspaceFolder}/dist/**/*.js"],
  "resolveSourceMapLocations": ["${workspaceFolder}/**", "!**/node_modules/**"]
}
```

### Chrome DevTools

1. Open **Sources** → confirm file tree matches workspace paths.
2. Breakpoint on **compiled** file first — if hits, source map is wrong.
3. **Disable cache** + hard reload when debugging service workers.

### Node inspect

```bash
node --inspect-brk -r ts-node/register src/index.ts
# chrome://inspect → Open dedicated DevTools
```

### Webpack `devtool` for bindable maps

```javascript
module.exports = {
  devtool: 'source-map', // not false in dev
};
```

## Mistakes to Avoid
> [!WARNING]
> **Optimizers (Terser)** drop unreachable code — breakpoint in removed branch stays unbound forever.

- **Mistake:** **Hot reload (Vite/HMR)** replaces modules
- **Mistake:** **Inline source maps** huge but bind reliably
- **Mistake:** **Breakpoint in `node_modules`**

| Symptom | Check | Fix |
|---------|-------|-----|
| Hollow breakpoint, never hits | File not in `outFiles` glob | Widen glob; check `dist/` output path |
| Hits wrong line | Column/line offset in map | Rebuild; align TS `sourceRoot` |
| Works after first request | Lazy import | Break in loader or entry chunk |
| Unbound in monorepo package | `link:` / workspace paths | `resolveSourceMapLocations` include package |
| Conditional breakpoint unbound | Syntax in condition | Simplify `x > 1` test |
| Docker path mismatch | `/app` vs local | `localRoot` / `remoteRoot` in launch.json |

## Pros/Cons or Trade-offs
- Don't fight unbound breakpoints in minified production without source maps
