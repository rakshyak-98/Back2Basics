[[Nginx]]

# nginx core functionality

> nginx core functionality — all workers processes get simultaneously notified about a new incoming connection.

---

## Mental model

**Say it in one breath:** nginx core functionality is infra/security tooling — least privilege, clear config, observable failures.


`accept_mutex`
When `accept_mutex` disabled
- All workers processes get simultaneously notified about a new incoming connection.
- the race to call `accept()` on the shared listen socket.
- Only one of them actually gets the connection.
- The others get `EAGAIN` (or similar) and go back to sleep.
This is called **thundering herd** problem (or wake-up storm).

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **nginx core functionality** | Core idea of this note | “I can explain nginx core functionality without jargon.” |
| **least privilege** | Only needed access | “Grant the smallest role that works.” |
| **secret** | Password/key/token | “Secrets out of git; rotate them.” |
| **observability** | metrics/logs/traces | “You can’t fix what you can’t see.” |

---

## Standard config / commands

```bash
# status
# check version, auth, and recent changes
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth fail | clock / creds / IAM | Sync time; fix policy |
| TLS error | cert chain / SNI | Fix certs and CA bundle |
| Deploy down | rollback / health | Roll back; check probes |

---

## Gotchas

> [!WARNING]
> Never commit long-lived secrets.

---

## When NOT to use

- Don’t build custom infra when managed services meet the SLO.

---

## Related

[[Nginx]]
