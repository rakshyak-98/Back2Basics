[[Descriptive]] [[DAP (Debug Adapter Protocol)]] [[Debugger configuratoin]]

# LSP

> LSP (Language Server Protocol) gives editors completions, go-to-def, and diagnostics via a language server process.





## Interview Relevance
Interviewers contrast LSP with DAP — language intelligence (completions, diagnostics) versus debugging. Expect capability negotiation and why the editor stays thin.

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview
- [Language Server Protocol specification](https://microsoft.github.io/language-server-protocol/) — deep-dive
- [LSP overview — Microsoft](https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/) — overview

## Key Concepts
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

## Technical Details
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

## Pros/Cons or Trade-offs
- **Tiny throwaway script in notepad** — overkill.
- **Formatting only** — formatter CLI may suffice.

## Mistakes to Avoid
> [!WARNING]
> **Multiple language servers** — fight over the same file type.

> [!WARNING]
> **LSP isn’t runtime** — green squiggles ≠ tests passed.

| Symptom | Check | Fix |
|---------|-------|-----|
| No completions | server not started | Install/enable extension |
| Wrong diagnostics | bad root | Open correct workspace folder |
| Stale types | server crash/cache | Restart LSP |
| Slow IDE | huge project | Exclude build dirs |
