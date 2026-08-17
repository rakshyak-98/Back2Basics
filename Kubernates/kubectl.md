[[Pods]] [[kubectl pod creation]] [[ingress]] [[Kubernetes services]] [[Kubernetes config]] [[Cilium]]

# kubectl

> `kubectl` is the CLI to the Kubernetes API — read cluster state, apply manifests, and debug failing pods through the apiserver (not by SSHing to nodes first).

```txt
        kubectl ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers watch context/namespace discipline, CrashLoop/ImagePull triage, …

## Sources
- [Kubernetes — kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) — overview
- [Kubernetes — Troubleshooting Applications](https://kubernetes.io/docs/tasks/debug/debug-application/) — deep-dive
- Brendan Burns et al., *Kubernetes: Up and Running* — overview

## Key Concepts
- **API objects:** Pod, Service, Deployment… — `kubectl` is CRUD + watch + port-forward + debug.
- **Context / namespace:** always know where you point ([[Kubernetes config]]).
- **Controllers reconcile:** Deployment → ReplicaSet → Pod; deleting a Pod under a Deployment respawns it.
- **Readiness = LB membership:** flaky readiness empties Endpoints → 502/503 at [[ingress]].

## Technical Details
```
kubectl ──► kube-apiserver ──► etcd (desired state)
                │
                ├── controllers reconcile
                └── kubelet on nodes runs containers
```

```bash
kubectl config current-context
kubectl config use-context prod-east
kubectl -n prod …

# Inventory + events
kubectl get pods -A -o wide
kubectl get deploy,sts,ds,svc,ingress -n prod
kubectl describe pod -n prod api-7f8b9c-xyz
kubectl get events -A --sort-by='.lastTimestamp' | tail -20

# Logs
kubectl logs -n prod api-xyz --since=10m
kubectl logs -n prod api-xyz --previous --tail=80
kubectl logs -n prod -l app=api --prefix --timestamps

# Apply / rollouts
kubectl apply -f deploy/
kubectl rollout status deployment/api -n prod
kubectl rollout undo deployment/api -n prod
kubectl set image deployment/api api=myreg/api:v2 -n prod

# Debug
kubectl exec -it -n prod api-xyz -- sh
kubectl debug -n prod api-xyz -it --copy-to=api-debug --image=nicolaka/netshoot --target=api
kubectl port-forward -n prod svc/api 8080:80

# jsonpath
kubectl get pods -n prod -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
```

- Bare Pod creation → [[kubectl pod creation]].

### CrashLoopBackOff triage

| Step | Command | Look for |
|------|---------|----------|
| 1 | `kubectl describe pod` | OOMKilled, Exit Code, Events |
| 2 | `kubectl logs --previous` | Last crash stack |
| 3 | Pod YAML probes/command | Liveness killing during boot |
| 4 | Limits vs RSS | Memory too low |
| 5 | ConfigMap/Secret mounts | Missing keys |

- Use `startupProbe` for slow boots

### Scaling chain

```
Traffic ↑ → HPA → Pending pods → CA nodes → pull/boot → Ready → Endpoints
```

```bash
kubectl get deploy,hpa,pdb -n prod -l app=api
kubectl describe hpa -n prod api
kubectl get events -n prod --field-selector reason=FailedScheduling | tail -10
kubectl top nodes
```

| Symptom | Check | Fix |
|---------|-------|-----|
| CrashLoopBackOff | logs `--previous`, describe | Fix exit; probes; secrets |
| ImagePullBackOff | Failed to pull | Tag/registry; `imagePullSecrets` |
| Pending | scheduling events | Resources; taints; PVC |
| Running not Ready | readiness | Fix `/ready`; dependency |
| 502 from ingress | endpoints empty | Readiness; selector |
| HPA stuck at min | `FailedGetResourceMetric` | metrics-server; set CPU **requests** |
| HPA at max, still slow | top pods; queue | Raise max; faster startup; KEDA |
| Scale-up, no Ready | FailedScheduling / CA | Node pool max; taints; image pull |
| Cross-service timeout | netpol; DNS FQDN | [[Cilium]] Hubble; `svc.ns.svc.cluster.local` |

## Mistakes to Avoid
- **Mistake:** Deleting Pods under a Deployment as a “fix” without changing the…
- **Mistake:** `logs` without `--previous` on CrashLoop
- **Mistake:** HPA without `resources.requests.cpu`
- **Mistake:** Using `localhost` for cross-service calls
- **Mistake:** Leaving ephemeral `kubectl debug` copies around
- **Mistake:** Scaling during a rollout without PDB/`maxSurge` headroom

## Pros/Cons or Trade-offs
- **Pro:** Fastest path to API truth (Events, describe, previous logs).
- **Con:** Laptop `kubectl` is not a deploy pipeline — use GitOps/CI.
- **Con:** `kubectl edit` drifts from Argo/Flux source of truth.

## Comparison
- vs SSH to nodes: prefer `kubectl debug` / exec; node debug is last resort.
- vs cloud console: kubectl is scriptable and closer to the API object model.


### Use cases
- On-call pod triage, rollout undo after bad image, and live HPA/endpoint watch…

- **Example:** Ingress 503 → empty Endpoints → readiness failing on `/ready` be…
