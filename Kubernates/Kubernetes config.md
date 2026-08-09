[[Kubernates]]

# You are essentially reading from or writing to etcd through the kubernetes API server.

> You are essentially reading from or writing to etcd through the kubernetes API server. — etcd — highly reliable, distributed key-value store that serves as…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** You are essentially reading from or writing to etcd through the kubernetes API server. is infra/security tooling — least privilege, clear config, observable failures.


etcd -> highly reliable, distributed key-value store that serves as the central data store and brain of Kubernetes.
- highly-available key-value database designed specifically for distributed systems. It stores all critical configuration data, metadata, and the current state of the Kubernetes cluster.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **You are essentially reading from or writing to etcd through the kubernetes API server.** | Core idea of this note | “I can explain You are essentially reading from or writing to etcd through the kubernetes API server. without jargon.” |
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

[[Kubernates]]
