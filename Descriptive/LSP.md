[[Descriptive]] [[DAP (Debug Adapter Protocol)]] [[Debugger configuratoin]]

# LSP

> LSP (Language Server Protocol) gives editors completions, go-to-def, and diagnostics via a language server process.

---

## Mental model

**Say it in one breath:** Editor speaks JSON-RPC to a server that understands the language — one server, many editors.

```txt
Editor ↔ LSP (JSON-RPC) ↔ language server (tsc, pylsp, gopls)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **language server** | Analysis process | “gopls for Go.” |
| **diagnostics** | Squiggles | “Push as you type.” |
| **capabilities** | What server supports | “Negotiate on init.” |
| **vs DAP** | Debug ≠ language smarts | “DAP for breakpoints.” |

---

## Standard config / commands

```bash
# examples
gopls version
pylsp --help
# editor: install extension that starts the server
```

| Knob | Why it matters |
|------|----------------|
| Root / workspace | Wrong root → missing imports |
| `settings.json` | Server config |
| Memory | Big monorepos need tuning |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No completions | server not started | Install/enable extension |
| Wrong diagnostics | bad root | Open correct workspace folder |
| Stale types | server crash/cache | Restart LSP |
| Slow IDE | huge project | Exclude build dirs |

---

## Gotchas

> [!WARNING]
> **Multiple language servers** — fight over the same file type.

> [!WARNING]
> **LSP isn’t runtime** — green squiggles ≠ tests passed.

---

## When NOT to use

- **Tiny throwaway script in notepad** — overkill.
- **Formatting only** — formatter CLI may suffice.

## Related

[[DAP (Debug Adapter Protocol)]] [[Debugger configuratoin]]
