[[Pods]] [[ingress]] [[Kubernetes services]] [[Kubernetes config]] [[Cilium]]

# kubectl

> CLI to the Kubernetes API — read cluster state, ship manifests, debug failing pods — **Kubernetes: Up and Running** (Burns et al.) + **The Kubernetes Book** (Sayed).

## Mental model

```
kubectl ──► kube-apiserver ──► etcd (desired state)
                │
                ├── controllers reconcile (Deployment → ReplicaSet → Pod)
                └── kubelet on nodes runs containers
```

Everything is an **API object** (Pod, Service, Deployment…). `kubectl` = CRUD + watch + port-forward + debug hooks.

**Context / namespace** — always know where you're pointing:

```bash
kubectl config current-context
kubectl config get-contexts
kubectl config use-context prod-east
export KUBECTL_CONTEXT=prod-east   # optional
kubectl -n prod …                  # override default namespace
```

## Standard config / commands

### Read state (80% of on-call)

```bash
# Inventory
kubectl get pods -A -o wide
kubectl get deploy,sts,ds,svc,ingress -n prod

# Detail + events (Events section = gold)
kubectl describe pod -n prod api-7f8b9c-xyz
kubectl describe node worker-2

# Events cluster-wide, sorted
kubectl get events -A --sort-by='.lastTimestamp' | tail -20

# Logs
kubectl logs -n prod api-7f8b9c-xyz --since=10m
kubectl logs -n prod api-7f8b9c-xyz -c sidecar -f --tail=100
kubectl logs -n prod -l app=api --prefix --timestamps --max-log-requests=10
```

### Apply / rollouts

```bash
kubectl apply -f deploy/
kubectl rollout status deployment/api -n prod
kubectl rollout history deployment/api -n prod
kubectl rollout undo deployment/api -n prod
kubectl set image deployment/api api=myreg/api:v2 -n prod
```

### jsonpath / custom columns (scriptable)

```bash
# Pod phases only
kubectl get pods -n prod -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'

# Image per container
kubectl get pods -n prod -o jsonpath='{range .items[*]}{.metadata.name}{": "}{range .spec.containers[*]}{.image}{", "}{end}{"\n"}{end}'

# Ready condition message
kubectl get pod -n prod api-xyz -o jsonpath='{.status.conditions[?(@.type=="Ready")].message}'

# All containers not Ready
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,READY:.status.containerStatuses[*].ready
```

### Debug / ephemeral access

```bash
# Shell in running pod
kubectl exec -it -n prod api-xyz -- sh

# Debug container (K8s 1.23+ beta, GA later) — when main image has no shell
kubectl debug -n prod api-xyz -it --copy-to=api-debug --container=debugger \
  --image=nicolaka/netshoot --target=api

# Node issues — privileged debug pod on host namespaces
kubectl debug node/worker-2 -it --image=nicolaka/netshoot -- chroot /host bash

# Port forward local → service
kubectl port-forward -n prod svc/api 8080:80
```

## CrashLoopBackOff triage

```
CrashLoopBackOff → container starts → exits non-zero → backoff retry
```

| Step | Command | Look for |
|------|---------|----------|
| 1 | `kubectl describe pod <p>` | `Last State: Terminated`, `Reason: OOMKilled`, `Exit Code`, Events |
| 2 | `kubectl logs <p> --previous` | Stack trace from *last* crash (current may be empty) |
| 3 | `kubectl get pod <p> -o yaml` | `livenessProbe` killing too early; wrong `command` |
| 4 | Compare limits | `resources.limits.memory` vs actual RSS |
| 5 | Config | `ConfigMap`/`Secret` mount paths; missing env |

```bash
# Quick loop
POD=api-xyz NS=prod
kubectl describe pod -n $NS $POD | tail -30
kubectl logs -n $NS $POD --previous --tail=80
kubectl get pod -n $NS $POD -o jsonpath='{.status.containerStatuses[0].lastState.terminated}'
```

**Common fixes:** raise memory limit; fix app startup (DB not ready → use init container / probe `startupProbe`); wrong entrypoint; missing secret key → file not found exit 1.

### Probe gotchas

```yaml
startupProbe:          # slow JVM/ML apps — don't liveness-kill during boot
  httpGet:
    path: /health
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  periodSeconds: 10
readinessProbe:        # removed from Service endpoints when failing
  httpGet:
    path: /ready
    port: 8080
```

## Triage table

| Symptom | Check | Fix |
|---------|-------|-----|
| CrashLoopBackOff | logs `--previous`, describe | Fix exit reason; probes; secrets |
| ImagePullBackOff | describe → `Failed to pull` | Tag/registry creds; `imagePullSecrets` |
| Pending | describe → scheduling | Resources; taints; PVC bind |
| Running not Ready | readiness probe logs | Fix `/ready`; dependency down |
| 502 from ingress | endpoints empty | Readiness failing; selector mismatch |
| Works locally, fails cluster | `kubectl exec` DNS/curl | NetworkPolicy; wrong service name |
| Random restarts | OOMKilled in describe | Raise limit or fix leak |

## Gotchas

> [!WARNING]
> **`kubectl delete pod` on Deployment** — pod respawns; fix Deployment template, not individual pod long-term.

> [!WARNING]
> **`logs` without `--previous`** on CrashLoop — empty or mid-boot noise; always check previous instance.

- **Default namespace** — prod objects in `default` = footgun; enforce `-n` or `kubectl-ns` plugin.
- **describe Events scroll off** — `--sort-by` on events or use `kubectl get events --field-selector involvedObject.name=…`
- **Ephemeral debug copies** — clean up `api-debug` pods; they hold resources.
- **jsonpath quoting** — use single quotes outside, double inside `{...}`.
- **Large manifest apply** — server-side apply (`kubectl apply --server-side`) reduces field manager conflicts.

## When NOT to use

- **GitOps drift repair via manual edit** — `kubectl edit` untracked; fix source repo (Argo/Flux).
- **Production scale exec** — use break-glass audit; prefer observability over SSH-via-kubectl habit.
- **Replacing CI deploy** — kubectl from laptop is not a pipeline.

## Related

[[Pods]] [[ingress]] [[Kubernetes services]] [[Kubernetes config]] [[Cilium]] [[Docker compose]]
