[[Pods]] [[ingress]] [[Kubernetes services]] [[Kubernetes config]] [[Cilium]] [[distributed system]] [[orchestration]]

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

## Multi-scaling systems (real-time triage)

Scaling incidents are rarely "HPA broken" — they're **capacity lag**: traffic spikes before pods schedule, images pull, JVM warms, or readiness passes. Debug the **whole chain** (metrics → HPA → scheduler → node pool → probes → endpoints).

```
Traffic ↑ → HPA scales Deployment → Pending pods → CA adds nodes → pull + boot → Ready → Endpoints
                │                      │                │              │
                └── metrics lag        └── quota/taints └── slow AMI    └── 503 until here
```

### Scaling inventory (run first)

```bash
NS=prod APP=api

# Workload + desired vs ready
kubectl get deploy,hpa,pdb -n $NS -l app=$APP
kubectl get pods -n $NS -l app=$APP -o wide --sort-by='.metadata.creationTimestamp'

# HPA decision inputs (current vs target)
kubectl describe hpa -n $NS $APP
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/namespaces/$NS/pods" | jq '.items[] | select(.metadata.name|test("'$APP'")) | {name:.metadata.name, cpu:.containers[].usage.cpu, mem:.containers[].usage.memory}'

# Scheduler / capacity
kubectl get events -n $NS --field-selector reason=FailedScheduling --sort-by='.lastTimestamp' | tail -10
kubectl top nodes
kubectl get nodes -o custom-columns=NAME:.metadata.name,READY:.status.conditions[-1].type,CPU:.status.allocatable.cpu,MEM:.status.allocatable.memory,TAINTS:.spec.taints

# Cluster autoscaler signals (events + unschedulable)
kubectl get events -A --field-selector reason=NotTriggerScaleUp,reason=TriggeredScaleUp --sort-by='.lastTimestamp' | tail -15
```

### HPA — symptom → check → fix

| Symptom | Check | Fix |
|---------|-------|-----|
| Replicas stuck at min | `describe hpa` → `FailedGetResourceMetric` | Install/fix **metrics-server**; verify `resources.requests.cpu` set (HPA needs requests, not just limits) |
| HPA at max, still high latency | `kubectl top pods`; app queue depth | Raise `maxReplicas`; tune target %; fix slow startup; add KEDA on queue lag |
| HPA flapping | `kubectl get hpa -w`; Events on Deployment | Widen stabilization window (`behavior.scaleDown/scaleUp`); fix noisy metric |
| Scale-up but no new Ready pods | Pending + FailedScheduling events | Cluster Autoscaler max; instance types; taints; PVC zone bind |
| Scale-up during deploy = chaos | `rollout status`; old + new pods | `maxSurge`/`maxUnavailable`; PDB blocking drain |
| CPU low but HPA won't scale down | `behavior.scaleDown.stabilizationWindowSeconds` | Expected — wait window; check custom metrics still high |

```bash
# HPA YAML knobs (v2)
# metrics: cpu 70% OR custom (Prometheus adapter / KEDA ScaledObject)
# behavior.scaleDown.stabilizationWindowSeconds: 300  # prevent thrash
# minReplicas / maxReplicas — max must cover peak + headroom for rollouts

kubectl get hpa -n prod -o yaml | yq '.items[] | {name: .metadata.name, min: .spec.minReplicas, max: .spec.maxReplicas, current: .status.currentReplicas, desired: .status.desiredReplicas, conditions: .status.conditions}'
```

### Cluster / node scaling

| Symptom | Check | Fix |
|---------|-------|-----|
| Pods Pending `Insufficient cpu/memory` | `describe pod` Events; `kubectl top nodes` | CA node group max; bigger instance type; reduce requests |
| Pods Pending `didn't match Pod's node affinity` | Pod affinity / topology spread | Fix zone spread vs single-AZ node pool |
| CA not adding nodes | CA logs; `NotTriggerScaleUp` events | Max nodes hit; GPU/special SKU unavailable; expand ASG/MIG |
| Nodes Added but pods still Pending | Image pull; init container; PVC | `describe pod`; fix registry; pre-pull DS; storage class AZ |
| Scale-down evicts wrong pods | PDB; `safe-to-evict` annotation | Tighten PDB `minAvailable`; mark long-batch jobs `safe-to-evict: "false"` |

```bash
# Pod Disruption Budget — rollout + drain guardrail
kubectl get pdb -n prod
kubectl describe pdb -n prod api-pdb
# spec.minAvailable: 80%  OR  minAvailable: 3  — blocks voluntary eviction below floor

# Rollout under load
kubectl rollout status deployment/api -n prod --timeout=5m
kubectl get rs -n prod -l app=api -o wide   # multiple ReplicaSets = canary or stuck rollout
```

### Live watch during incident

```bash
# Terminal 1 — replica + endpoint health
watch -n2 'kubectl get deploy,hpa,pods,endpoints -n prod -l app=api'

# Terminal 2 — scheduling + HPA events
kubectl get events -n prod --watch --field-selector involvedObject.kind=HorizontalPodAutoscaler
kubectl get events -n prod --watch | grep -E 'FailedScheduling|TriggeredScaleUp|Unhealthy'

# Terminal 3 — ingress/controller 502 correlation
kubectl logs -n ingress-nginx deploy/ingress-nginx-controller --since=5m | grep -E '502|upstream'
```

## Microservices (real-time triage)

In microservice meshes, **kubectl proves the platform path** before you blame app code: DNS → Service → Endpoints → NetworkPolicy → (mesh route) → target Pod. One broken hop looks like "random 503s."

```
Client pod ──DNS──► svc.other-ns.svc.cluster.local:8080
                         │
                         ├── Endpoints (only Ready pods)
                         ├── NetworkPolicy allow?
                         ├── Ingress / Gateway API
                         └── mTLS / VirtualService (if mesh)
```

### Service graph (run first)

```bash
NS=prod
# All services + whether they have backends
kubectl get svc,endpointslices -n $NS -o wide
kubectl get endpoints -n $NS -o custom-columns=NAME:.metadata.name,ENDPOINTS:.subsets[*].addresses[*].ip,NOTREADY:.subsets[*].notReadyAddresses[*].ip

# Who calls whom — pick client pod, test path
CLIENT=$(kubectl get pod -n $NS -l app=checkout -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n $NS $CLIENT -- sh -c 'getent hosts orders.prod.svc.cluster.local; nc -zv orders.prod.svc.cluster.local 8080 2>&1 | head -1'

# Cross-namespace
kubectl exec -n $NS $CLIENT -- curl -sS -m3 -o /dev/null -w '%{http_code}\n' http://orders.other-ns.svc.cluster.local:8080/health
```

### Microservice symptom → check → fix

| Symptom | Check | Fix |
|---------|-------|-----|
| Intermittent 503 from ingress | `kubectl get endpoints`; readiness | Failing readiness on subset of pods; fix dependency timeout |
| `Connection refused` pod-to-pod | Service port vs `targetPort`; named port drift | Align `port`/`targetPort`; redeploy with consistent port names |
| DNS works, TCP fails | NetworkPolicy ingress/egress | `kubectl get netpol -n $NS -o yaml`; allow client namespace label |
| Only fails cross-AZ | Topology spread + single-replica dependency | Spread constraints; scale dependency; avoid hard AZ pin without peers |
| Works via Service, fails pod IP | Expected if policy allows only via Service | Call via DNS name; fix mesh routing |
| One version gets traffic after deploy | Multiple ReplicaSets / labels | `kubectl get rs -l app=api`; fix selector; complete rollout |
| Cascading failure (many svcs red) | Shared dependency (DB, auth, config) | `kubectl logs` on shared svc; `kubectl get configmap,secret` versions |
| Timeouts under load | `kubectl top pods`; HPA lag | Scale callee; tune client timeouts/retries; bulkhead at app layer |
| mTLS / mesh 503 URX | Sidecar inject? `istioctl proxy-status` | Missing sidecar; wrong DestinationRule subset |

### Multi-service debug workflow

```bash
# 1) Map blast radius — which deployments share a label/namespace
kubectl get deploy -n prod -o custom-columns=NAME:.metadata.name,READY:.status.readyReplicas,DESIRED:.status.replicas,AGE:.metadata.creationTimestamp

# 2) Correlate by time — cluster events around incident
kubectl get events -n prod --sort-by='.lastTimestamp' | tail -30

# 3) Same trace ID across pods (if app logs trace_id)
kubectl logs -n prod -l app=gateway --since=10m | grep 'trace_id=abc123'
kubectl logs -n prod -l app=orders --since=10m | grep 'trace_id=abc123'

# 4) Config drift between replicas
for p in $(kubectl get pods -n prod -l app=api -o name); do
  echo "=== $p ==="
  kubectl exec -n prod $p -- printenv | grep -E 'FEATURE_|DB_|REDIS_' | sort
done

# 5) Ephemeral traffic capture (netshoot sidecar/debug)
kubectl debug -n prod $CLIENT -it --image=nicolaka/netshoot --target=checkout -- tcpdump -i any port 8080 -c 20
```

### Canary / blue-green from kubectl

```bash
# Two deployments, one Service — check selector overlap
kubectl get deploy,svc -n prod -l 'app in (api,api-canary)' -o wide
kubectl describe svc api -n prod | grep -A5 Selector

# Weighted traffic usually needs mesh/ingress annotation — verify backend pods
kubectl get pods -n prod -l version=canary -o wide
kubectl get endpoints api -n prod -o yaml | yq '.subsets[].addresses | length'
```

### Standard microservice kubectl kit

| Goal | Command |
|------|---------|
| Prove DNS | `kubectl exec … -- getent hosts <svc>.<ns>.svc.cluster.local` |
| Prove TCP | `kubectl exec … -- nc -zv <host> <port>` |
| Prove HTTP | `kubectl exec … -- curl -sS -m3 -o /dev/null -w '%{http_code}\n' http://<host>:<port>/health` |
| Prove endpoints | `kubectl get endpoints <svc> -n <ns>` |
| Prove policy | `kubectl describe netpol -n <ns>` + temporary allow-all in staging only |
| Prove rollout | `kubectl rollout status deploy/<name> -n <ns>` |
| Prove quota | `kubectl describe resourcequota -n <ns>` |

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
| Traffic spike, elevated 5xx | HPA status; endpoints count; `top pods` | Scale max; reduce startup time; PDB + surge tuning |
| HPA not scaling | `describe hpa`; metrics-server | Set CPU requests; fix metrics adapter |
| Pods Pending after scale-up | FailedScheduling events; CA events | Raise node pool; fix affinity; quotas |
| One microservice down takes out many | Shared ConfigMap/Secret; dependency SLO | Isolate config versions; timeout + bulkhead in callers |
| Cross-service timeout only in prod | netpol; mesh mTLS; wrong namespace DNS | Allow egress/ingress; FQDN `svc.ns.svc.cluster.local` |
| After deploy, mixed old/new behavior | ReplicaSets; endpoint subsets | Finish rollout; verify single label selector on Service |

## Gotchas

> [!WARNING]
> **`kubectl delete pod` on Deployment** — pod respawns; fix Deployment template, not individual pod long-term.

> [!WARNING]
> **`logs` without `--previous`** on CrashLoop — empty or mid-boot noise; always check previous instance.

> [!WARNING]
> **HPA without resource requests** — CPU-based HPA ignores pods with no `resources.requests.cpu`; looks "broken" while load climbs.

> [!WARNING]
> **Scaling + rolling update overlap** — new pods compete for cluster capacity with surge pods; combine `maxSurge: 25%` + PDB + realistic `minReplicas` headroom.

> [!WARNING]
> **Readiness = load balancer membership** — flaky readiness during scale removes endpoints mid-request → 502 storm at ingress; use `startupProbe` and dependency checks that match real traffic paths.

> [!WARNING]
> **Microservice DNS is not localhost** — `localhost:8080` in pod A is not service B; use `http://<svc>.<ns>.svc.cluster.local:<port>`.

- **Default namespace** — prod objects in `default` = footgun; enforce `-n` or `kubectl-ns` plugin.
- **describe Events scroll off** — `--sort-by` on events or use `kubectl get events --field-selector involvedObject.name=…`
- **Ephemeral debug copies** — clean up `api-debug` pods; they hold resources.
- **jsonpath quoting** — use single quotes outside, double inside `{...}`.
- **Large manifest apply** — server-side apply (`kubectl apply --server-side`) reduces field manager conflicts.
- **EndpointSlices vs Endpoints** — `kubectl get endpoints` may truncate; use `endpointslices` for large fleets (many microservice replicas).
- **Custom metrics lag** — Prometheus adapter / KEDA can be 30–60s behind; don't expect instant scale on queue depth.

## When NOT to use

- **GitOps drift repair via manual edit** — `kubectl edit` untracked; fix source repo (Argo/Flux).
- **Production scale exec** — use break-glass audit; prefer observability over SSH-via-kubectl habit.
- **Replacing CI deploy** — kubectl from laptop is not a pipeline.

## Related

[[Pods]] · [[ingress]] · [[Kubernetes services]] · [[Kubernetes config]] · [[Cilium]] · [[Docker compose]] · [[orchestration]] · [[distributed system]] · [[connection chrun]]
