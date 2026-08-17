[[Pods]] [[kubectl]] [[Kubernetes config]] [[Kubernetes services]] [[ingress]] [[Cilium]]

# kubectl pod creation

> Create a Pod through the API — declarative manifests (preferred), generated YAML from `kubectl run --dry-run`, or imperative one-offs for debug only.





## Interview Relevance
Interviewers contrast bare Pods versus Deployments, `apply` versus `create`, and probes/resources that keep Pods schedulable and Ready.

## Sources
- [Kubernetes — Pods](https://kubernetes.io/docs/concepts/workloads/pods/) — deep-dive
- [Kubernetes — Imperative commands](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/imperative-command/) — overview
- Brendan Burns et al., *Kubernetes: Up and Running* — overview

## Key Concepts
- **API object, not direct container run:** apiserver → etcd → scheduler → kubelet.
- **Bare Pod ≠ self-healing:** node loss/eviction does not recreate it — use Deployment/StatefulSet/Job for real workloads.
- **`apply` upserts; `create` 409s** on re-run — CI/GitOps want apply.
- **Requests schedule; limits cap; probes gate traffic.**

## Technical Details
```
kubectl run / apply ──► kube-apiserver ──► etcd
                              │
                         scheduler assigns node
                              │
                         kubelet starts containers
```

| Path | When |
|------|------|
| `kubectl apply -f` | Anything that should survive the afternoon |
| `kubectl run` + `--dry-run=client -o yaml` | Bootstrap then edit |
| `kubectl run` (live) | Throwaway debug — avoid in prod |
| `kubectl create -f` | One-shot; fails on duplicate |

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: api-debug
  namespace: prod
  labels: { app: api, tier: debug }
spec:
  restartPolicy: Never
  containers:
    - name: api
      image: myreg/api:1.2.3
      ports: [{ name: http, containerPort: 8080 }]
      env:
        - name: DB_URL
          valueFrom:
            secretKeyRef: { name: api-secrets, key: db-url }
      resources:
        requests: { cpu: 100m, memory: 128Mi }
        limits: { cpu: 500m, memory: 512Mi }
      readinessProbe:
        httpGet: { path: /ready, port: http }
      livenessProbe:
        httpGet: { path: /health, port: http }
```

```bash
kubectl run api-debug \
  --image=myreg/api:1.2.3 -n prod \
  --labels=app=api,tier=debug --port=8080 \
  --requests=cpu=100m,memory=128Mi \
  --limits=cpu=500m,memory=512Mi \
  --dry-run=client -o yaml > pod.yaml
kubectl apply -f pod.yaml

kubectl run tmp-shell -n prod --rm -it \
  --image=nicolaka/netshoot --restart=Never --command -- sleep 3600

kubectl apply --server-side -f pod.yaml
```

Multi-container: sidecars share Pod IP/volumes; cannot bind the same port. Init containers run to completion before mains.

| Symptom | Check | Fix |
|---------|-------|-----|
| `Forbidden` | `kubectl auth can-i create pods -n prod` | RoleBinding |
| `AlreadyExists` | existing name | Delete/rename or `apply` |
| Stuck `Pending` | describe Events | Taints; CPU/mem; PVC |
| `ImagePullBackOff` | Failed to pull | Tag; `imagePullSecrets` |
| `CreateContainerConfigError` | missing secret/configmap | Create object; fix key |
| `CrashLoopBackOff` | `logs --previous` | Command/env/probes → [[kubectl]] |
| No Service traffic | endpoints | Not Ready; label mismatch |
| YAML changes ignored | bare Pod immutability | Delete/recreate or use Deployment |

## Real-World Applications
Debug pods in prod namespaces, init wait-for-DB patterns, and generating manifests for GitOps from dry-run.

**Example:** `kubectl run … --dry-run=client -o yaml` → add probes/env → `apply` → confirm Ready before attaching a Service selector.

## Pros/Cons or Trade-offs
- **Pro:** Fast path to a running container for learning and break-glass.
- **Con:** Bare Pods do not scale or self-heal — wrong for app tiers.
- **Con:** Imperative `run` in shared clusters creates untracked objects.

## Comparison
- vs Deployment: use Deployment for replicas, rollouts, HPA.
- vs StatefulSet: ordered identity + stable storage.
- vs Jobs: finite run-to-completion with `restartPolicy: OnFailure/Never`.

## Mistakes to Avoid
- Production apps as standalone Pods.
- `kubectl run` without dry-run in shared clusters.
- Omitting namespace (lands in `default`).
- `:latest` tags and missing resource requests (BestEffort eviction).
- `kubectl create` in scripts that re-run.
- Two containers binding the same port in one Pod.
