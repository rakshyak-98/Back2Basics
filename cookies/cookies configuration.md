[[cross-site scripting]]

# cookies configuration

> cookies configuration — set-Cookie: sessionToken=abc123; Expires=Wed, 09 Jun 2024 10:18:14 GMT

---

## Mental model

**Say it in one breath:** cookies configuration — plain job, how I run it, how I know it’s broken.


[cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cookie)
```shell
HTTP/1.0 200 OK
Content-type: text/html
Set-Cookie: theme=light
Set-Cookie: sessionToken=abc123; Expires=Wed, 09 Jun 2024 10:18:14 GMT
httpOnly
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **cookies configuration** | Core idea of this note | “I can explain cookies configuration without jargon.” |
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

[[cross-site scripting]]
