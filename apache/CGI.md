[[apache]]

# CGI

> CGI — common Gateway Interface — is a standard protocol that allows a web server to interact with external programs (called CGI scripts or programs) to…

---

## Mental model

**Say it in one breath:** CGI — plain job, how I run it, how I know it’s broken.


Common Gateway Interface -> is a standard protocol that allows a web server to interact with external programs (called CGI scripts or programs) to generate dynamic content, rather than just serving static files.
Process per request -> Each CGI invocation spawns a new process, which is resource-intensive (slow for high traffic). This is why modern alternatives like FastCGI, mod_php, or application servers (Node.js) are preferred.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **CGI** | Core idea of this note | “I can explain CGI without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[apache]]
