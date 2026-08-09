[[apache]]

# fastCGI servers

> fastCGI servers — fast Common Gateway Interface — binary protocol that improves upon the original CGI by providing a high-performance, language-agnostic way…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** fastCGI servers — plain job, how I run it, how I know it’s broken.


Fast Common Gateway Interface -> binary protocol that improves upon the original CGI by providing a high-performance, language-agnostic way for web servers to interface with external applications for generating dynamic content.
- Process that handles dynamic content generation (like php, python etc.) and communicates with web servers (like Nginx) via the FastCGI protocol.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **fastCGI servers** | Core idea of this note | “I can explain fastCGI servers without jargon.” |
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
