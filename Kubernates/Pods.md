<!-- note-strategy: operational -->
[[kubectl]] [[kubectl pod creation]] [[Kubernetes services]] [[ingress]]

# Pods

> Smallest schedulable unit — one or more containers sharing network and volumes — **Kubernetes: Up and Running** (Burns et al.).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Smallest schedulable unit — one or more containers sharing network and volumes — **Kubernetes: Up and Running** (Burns et al.).

## Standard config / commands

```bash
kubectl get pods -A -o wide
kubectl describe pod my-pod -n default
kubectl logs my-pod -c app
kubectl delete pod my-pod --grace-period=0 --force   # last resort
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| CrashLoopBackOff | `kubectl logs --previous`; probe failures | Fix exit code; adjust command or probes |
| ImagePullBackOff | image name; pull secret | `kubectl describe pod`; fix registry auth |
| Pending | CPU/memory; PVC bind | `kubectl describe node`; check requests and storage class |
| Running but not Ready | readiness probe failing | Hit probe path from inside cluster |

---

## Gotchas

> [!WARNING]
> Restarting a Pod **creates a new identity** — IP and in-memory state are lost unless volumes back them.

---

## When NOT to use

- Do not run more than one main process per container — use sidecars for helpers.


---

## Related

[[kubectl]] · [[kubectl pod creation]] · [[Kubernetes services]] · [[ingress]]
