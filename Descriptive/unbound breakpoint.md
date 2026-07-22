[[Descriptive/vscode]] [[javascript]] [[NodeJS/node command]] [[compiler/library file]]

# Unbound breakpoint

> Debugger set a breakpoint but cannot map it to executable code yet — common with source maps, wrong path, or unloaded modules — **VS Code / Chrome DevTools playbook**.

## Mental model

A breakpoint is **bound** when the debugger links it to an exact script location (file URL + line → bytecode offset). **Unbound** means the IDE shows the breakpoint (often hollow/grey) but the runtime has no matching source line loaded.

```
IDE breakpoint (app.ts:42)
        │
        ▼ source map / path resolution
Runtime script (bundle.js)  ──► bound ✓
                         or ──► unbound ✗ (module not loaded, map mismatch)
```

Typical causes: typo path, webpack path prefix, breakpoint in dead code, lazy-loaded chunk not fetched yet.

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hollow breakpoint, never hits | File not in `outFiles` glob | Widen glob; check `dist/` output path |
| Hits wrong line | Column/line offset in map | Rebuild; align TS `sourceRoot` |
| Works after first request | Lazy import | Break in loader or entry chunk |
| Unbound in monorepo package | `link:` / workspace paths | `resolveSourceMapLocations` include package |
| Conditional breakpoint unbound | Syntax in condition | Simplify `x > 1` test |
| Docker path mismatch | `/app` vs local | `localRoot` / `remoteRoot` in launch.json |

## Gotchas

> [!WARNING]
> **Optimizers (Terser)** drop unreachable code — breakpoint in removed branch stays unbound forever.

- **Hot reload (Vite/HMR)** replaces modules — breakpoints may unbind until re-set.
- **Inline source maps** huge but bind reliably; external maps need correct `//# sourceMappingURL`.
- **Breakpoint in `node_modules`** — skipped unless `"skipFiles": false` and map exists.

## When NOT to use

- Don't fight unbound breakpoints in minified prod without source maps — use logging/tracing ([[Linux/loggging]]) instead.

## Related

[[Descriptive/vscode]] [[javascript]] [[NodeJS/node command]] [[Descriptive/JavaScript/execution context]]
