[[Kubernates]]

# Kubernetes services

> Kubernetes services — in Kubernetes, a service is a method for exposing a network application that is running as one or more Pods in your cluster.

---

## Mental model

**Say it in one breath:** Kubernetes services is infra/security tooling — least privilege, clear config, observable failures.


in Kubernetes, a service is a method for exposing a network application that is running as one or more [[Pods]] in your cluster.
A Service is an abstraction that defines a logical set of [[Pods]] and a policy to access them.
- It enables seamless communication between different parts of an application and external clients by providing a stable endpoint, even as the underlying Pods may change.
- Service decouple the frontend from backend Pods, ensuring consistent access despite Pod restarts or scaling operations
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
   app.kubernetes.io/name: MyApp
  ports:
   - port: 80
  # By default and for convenience, the `targetPort` is set to
  # the same value as the `port` field.
   targetPort: 80
   # Optional field
   # By default and for convenience, the Kubernetes control plane
   # will allocate a port from a range (default: 30000-32767)

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Kubernetes services** | Core idea of this note | “I can explain Kubernetes services without jargon.” |
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
