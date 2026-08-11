[[ssh]]

# ssh private network

> ssh private network — ip addr show | grep inet

---

## Mental model

**Say it in one breath:** ssh private network is infra/security tooling — least privilege, clear config, observable failures.


```bash
ip addr show | grep inet
```
**Remove any wide-open ssh rule**
```bash
sudo ufw delete allow 22;
sudo ufw delete allow ssh;
sudo ufw delete allow OpenSSH;
```
**Allow SSH only from your private network**
```bash
sudo ufw allow from 192.168.1.0/24 to any port 22 proto http
```
```bash
sudo ufw allow from 192.168.1.0/24 to any port ssh
sudo ufw allow from 192.168.1.0/24 port 22 proto tcp
```
**Reload `ufw`**
```bash
sudo ufw reload; # reload
sudo ufw status numbered; # verify the rule
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ssh private network** | Core idea of this note | “I can explain ssh private network without jargon.” |
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
