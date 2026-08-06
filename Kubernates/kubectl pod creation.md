[[Pods]] [[kubectl]] [[Kubernetes config]] [[Kubernetes services]] [[ingress]]

# kubectl pod creation

> Ship a Pod object through the API — imperative one-offs, declarative manifests, or generated YAML — **Kubernetes: Up and Running** (Burns et al.) + **The Kubernetes Book** (Sayed).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```
kubectl run / apply ──► kube-apiserver ──► etcd (Pod desired state)
                              │
                         scheduler assigns node
                              │
                         kubelet starts containers on that node
```

A **Pod** is the smallest deployable unit: one or more containers that share network and optional volumes. `kubectl` does not “run a container” on a node directly — it creates a **Pod API object**; controllers and kubelet do the rest.

| Path                                       | When                                                                      |
| ------------------------------------------ | ------------------------------------------------------------------------- |
| `kubectl apply -f`                         | Default for anything that survives the afternoon (GitOps, CI, repeatable) |
| `kubectl run` + `--dry-run=client -o yaml` | Bootstrap a manifest from flags, then edit and apply                      |
| `kubectl run` (no dry-run)                 | Quick throwaway pod in dev — avoid in prod                                |
| `kubectl create -f`                        | One-shot create; fails on duplicate name (no upsert)                      |

**Bare Pod vs Deployment:** a standalone Pod is not self-healing. Node loss or eviction does not recreate it. Production workloads almost always go through **Deployment** (or StatefulSet / Job). Bare Pods are for debug, batch one-offs, operators, or learning.

## Standard config / commands

### Declarative Pod (production-safe pattern)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: api-debug
  namespace: prod
  labels:
    app: api
    tier: debug
spec:
  restartPolicy: Never          # standalone Pod: Always still won't survive node loss
  containers:
    - name: api
      image: myreg/api:1.2.3    # pin tag — never :latest in prod
      imagePullPolicy: IfNotPresent
      ports:
        - name: http
          containerPort: 8080
      env:
        - name: LOG_LEVEL
          value: info
        - name: DB_URL
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: db-url
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 512Mi
      readinessProbe:
        httpGet:
          path: /ready
          port: http
        periodSeconds: 5
      livenessProbe:
        httpGet:
          path: /health
          port: http
        periodSeconds: 10
```

```bash
kubectl apply -f pod.yaml
kubectl get pod -n prod api-debug -w
kubectl describe pod -n prod api-debug
```

Annotate the knobs:
- **`restartPolicy`** — `Always` (default), `OnFailure`, `Never`. For Jobs/CronJobs use `OnFailure` or `Never`; Deployments ignore this on the Pod template (always `Always`).
- **`resources.requests`** — scheduler uses these for placement; omit → BestEffort QoS → first evicted under pressure.
- **`resources.limits`** — cgroup cap; OOM kills container when exceeded.
- **Probes** — readiness keeps bad pods out of Service endpoints; liveness restarts stuck containers.

### Generate YAML from imperative flags (recommended bootstrap)

```bash
kubectl run api-debug \
  --image=myreg/api:1.2.3 \
  --namespace=prod \
  --labels=app=api,tier=debug \
  --port=8080 \
  --requests=cpu=100m,memory=128Mi \
  --limits=cpu=500m,memory=512Mi \
  --dry-run=client -o yaml > pod.yaml
# edit pod.yaml (probes, env, volumes), then:
kubectl apply -f pod.yaml
```

`--dry-run=client` prints the manifest without calling the API — safe to pipe to a file.

### Imperative one-off (dev / break-glass only)

```bash
kubectl run tmp-shell -n prod --rm -it \
  --image=nicolaka/netshoot \
  --restart=Never \
  --command -- sleep 3600
```

`--rm` deletes the Pod when the session ends (interactive). Without `--rm`, clean up manually.

### Multi-container Pod (sidecar pattern)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-with-log-shipper
spec:
  containers:
    - name: nginx
      image: nginx:1.27
      ports:
        - containerPort: 80
      volumeMounts:
        - name: logs
          mountPath: /var/log/nginx
    - name: log-shipper
      image: fluent/fluent-bit:2.2
      volumeMounts:
        - name: logs
          mountPath: /var/log/nginx
          readOnly: true
  volumes:
    - name: logs
      emptyDir: {}
```

Sidecars share the Pod IP and can use `localhost`; they must not bind the same `containerPort`.

### Init containers (ordering before main starts)

```yaml
spec:
  initContainers:
    - name: wait-for-db
      image: busybox:1.36
      command: ['sh', '-c', 'until nc -z db 5432; do sleep 2; done']
  containers:
    - name: api
      image: myreg/api:1.2.3
```

Init containers run to completion (or failure) in order before any main container starts.

### apply vs create

```bash
kubectl create -f pod.yaml   # HTTP 409 if name exists
kubectl apply -f pod.yaml    # upsert — preferred for manifests in git
kubectl replace -f pod.yaml  # full replace; drops fields not in file if misused
```

For CI/GitOps, only **`apply`** (or server-side apply) is tracked; `create` is a footgun on re-runs.

### Server-side apply (field-manager conflicts)

```bash
kubectl apply --server-side -f pod.yaml
kubectl apply --server-side --force-conflicts -f pod.yaml   # break-glass only
```

Use when multiple actors (operator + human) touch the same object.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Forbidden` / RBAC error | `kubectl auth can-i create pods -n prod` | Grant `create pods`; check RoleBinding |
| `AlreadyExists` | `kubectl get pod -n prod <name>` | Delete old pod, rename, or use `apply` |
| Stuck `Pending` | `kubectl describe pod` → Events | Taints/tolerations; insufficient CPU/mem; PVC not bound |
| `ImagePullBackOff` | describe → `Failed to pull` | Wrong tag; private registry → `imagePullSecrets` |
| `CreateContainerConfigError` | describe → `secret/configmap not found` | Create Secret/ConfigMap; fix key name |
| `CrashLoopBackOff` right after create | `kubectl logs --previous` | Bad command; missing env; probe too aggressive → [[kubectl]] |
| Pod created but no Service traffic | `kubectl get endpoints` | Pod not Ready; labels don’t match Service selector → [[Kubernetes services]] |
| Changes to YAML ignored | `kubectl get pod -o yaml` vs file | Bare Pod is mostly immutable — delete and recreate, or use Deployment |

```bash
NS=prod POD=api-debug
kubectl describe pod -n $NS $POD | sed -n '/Events:/,$p'
kubectl get events -n $NS --field-selector involvedObject.name=$POD
kubectl get pod -n $NS $POD -o jsonpath='{.status.conditions[*].message}{"\n"}'
```

## Gotchas

> [!WARNING]
> **Standalone Pods are not recreated** — kubelet restarts containers per `restartPolicy`, but if the Pod object is deleted or the node dies, nothing brings it back. Use Deployment/StatefulSet for long-lived apps.

> [!WARNING]
> **`kubectl run` without dry-run** creates a live object — easy to forget in shared clusters. Prefer `dry-run=client -o yaml` → review → `apply`.

- **Default namespace** — objects land in `default` if `-n` omitted; enforce namespace in manifests (`metadata.namespace`).
- **`restartPolicy: Always` on bare Pod** — container restarts on crash, but Pod still has single-node lifetime; don’t confuse with Deployment resilience.
- **Port conflicts in multi-container Pods** — two containers cannot bind the same port on the shared network namespace.
- **`latest` image tag** — node may keep old cached image; pin semver or digest.
- **Immutable fields** — changing `spec.nodeName` or some volume bindings requires delete/recreate.
- **`kubectl create` in scripts** — second run fails; scripts should use `apply` or `kubectl apply --prune` in a controlled pipeline.

## When NOT to use

- **Production app tiers** — create a **Deployment** (or StatefulSet) instead; bare Pod creation is for debug, Jobs, or operator-managed objects.
- **Replacing GitOps** — manual `kubectl run` in prod drifts from Argo/Flux source; fix the repo.
- **Scaling** — bare Pods don’t scale; use Deployment `replicas` or HPA.
- **Stateful identity** — ordered storage + stable network ID → StatefulSet, not a hand-crafted Pod.

## Related

[[Pods]] [[kubectl]] [[Kubernetes config]] [[Kubernetes services]] [[ingress]] [[Cilium]] [[Docker compose]]
