[[ssh]]

# Verify with the public key

> Verify with the public key — TCP Connection — Your client connects to the server on port 22.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Verify with the public key is infra/security tooling — least privilege, clear config, observable failures.


```bash
ssh user@server.example.com
```
1. TCP Connection -> Your client connects to the server on port 22.
2. Protocol Negotiation -> They agree on which encryption/authentication algorithm to use.
3. Key Exchange -> They establish a shared secret for encrypting everything.
4. Server Authentication -> You verify you're talking to the real server.
5. Client Authentication -> The server verifies you are who you say you are.
6. Secure Session Established -> Encrypted communication tunnel is read.
**Generate Key Pair (Private + Public)**
```bash
ssh-keygen -t ed25519 -C "you@example.com"
```
- private keys stays with you, the server needs to know who it should trust so, you copy your public key `~/.ssh/authorized_key` of your account on the server.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Verify with the public key** | Core idea of this note | “I can explain Verify with the public key without jargon.” |
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

[[ssh]]
