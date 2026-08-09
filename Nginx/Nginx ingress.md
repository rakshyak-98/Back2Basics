[[Nginx]]

# Nginx ingress

> Nginx ingress — acts as a load balancer and Reverse Proxy for kubernetes cluster.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Nginx ingress is infra/security tooling — least privilege, clear config, observable failures.


Acts as a load balancer and [[Reverse Proxy]] for kubernetes cluster.
Nginx ingress is a ingress controller for Kubernetes that manages external access to services running in a kubernetes cluster.
- enables secure and scalable HTTP(S) traffic routing to Kubernetes workloads.
- rate limiting, IP whitelisting, and custom error page.
Load Balancing: Distributes traffic across multiple back-end pods to ensure reliability and scalability
SSL/TLS Termination: Handles HTTPS traffic by terminating SSL connections at the ingress layer.
Host-Based Routing: Routes requests based on URL paths or hostnames.
Authentication: Supports basic authentication, JWT, and OAuth2 integration.
### Example nginx ingress config file
```yaml
apiVersion: networking.k8s.io/v1 # must be appropriate version
kind: Ingress # Always set to Ingress
metadata:
	name: basic-ingress # Name of the ingress resource
spec:
	rules: # specifies at leat one routing rule (host and path)

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Nginx ingress** | Core idea of this note | “I can explain Nginx ingress without jargon.” |
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
