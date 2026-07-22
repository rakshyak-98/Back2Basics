[[Kubernetes services]] [[ingress]] [[kubectl]] [[Pods]]

# Cilium

> eBPF-powered CNI: pod networking, kube-proxy replacement, NetworkPolicy enforcement, Hubble observability — **Kubernetes: Up and Running** (Burns et al.) + Cilium docs.

## Mental model

Cilium sits at the **data plane** of Kubernetes networking:

```
Pod eth0 ──► veth ──► node eBPF (Cilium) ──► cluster routing / encap
                           │
                           ├── NetworkPolicy (L3/L4/L7)
                           ├── Service load-balancing (kube-proxy replacement)
                           └── Hubble: flow logs + metrics
```

**Why eBPF:** filter/NAT/route in kernel without iptables chain explosion at 5k+ Services.

Components on each node:

| Piece | Role |
|-------|------|
| **cilium-agent** | Programs eBPF maps, policy, endpoints |
| **cilium-operator** | IPAM, CRD reconciliation |
| **hubble-relay + ui** | Cluster-wide flow visibility |
| **cilium-envoy** (optional) | L7 policy / Ingress mesh features |

Pod identity = **labels**, not IP — policies survive restarts.

## Standard config / commands

### Verify install

```bash
kubectl -n kube-system get pods -l k8s-app=cilium
cilium status --wait          # cilium CLI on node or debug pod
kubectl -n kube-system exec ds/cilium -- cilium status
```

### Hubble (ops gold)

```bash
# Enable flows UI (if chart didn't)
helm upgrade cilium cilium/cilium -n kube-system --set hubble.enabled=true \
  --set hubble.relay.enabled=true --set hubble.ui.enabled=true

hubble observe --namespace prod --pod api-
hubble observe --protocol tcp --port 5432 --verdict DROPPED
hubble observe --from-label app=frontend --to-label app=api --follow
```

### NetworkPolicy (Cilium extends K8s NP)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-ingress
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

CiliumNetworkPolicy adds DNS-aware/L7 rules — use when standard NP insufficient.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: l7-api
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
          rules:
            http:
              - method: GET
                path: "/health"
```

### kube-proxy replacement check

```bash
kubectl -n kube-system exec ds/cilium -- cilium service list
# BPF LB maps should list ClusterIPs
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Pod `ContainerCreating` stuck | `kubectl describe pod`; Cilium IPAM events | Free CIDR; fix IPAM mode; restart agent |
| Service unreachable | `cilium service list`; endpoints | Missing backend pods; wrong selector; BPF LB disabled |
| Policy suddenly blocks traffic | `hubble observe --verdict DROPPED` | Label mismatch; namespace selector; add explicit allow |
| DNS timeouts | Hubble to kube-dns; CoreDNS policy | Allow udp/53 to kube-system; Cilium DNS policy |
| NodeNotReady after upgrade | `cilium status`; kernel ≥ requirement | Match Cilium version matrix; eBPF modules loaded |
| Cross-node pod fail | Encapsulation: VXLAN/GENEVE vs routing | Native routing needs L2 adjacency; fix underlay MTU |
| High CPU on cilium-agent | Map pressure, policy count | Split policies; upgrade; reduce L7 scope |
| Works with NP disabled | Confirm with `kubectl get netpol` | Default deny + explicit allows in zero-trust |

### Debug flow (SE playbook)

```bash
# 1. Endpoint health
kubectl -n kube-system exec ds/cilium -- cilium endpoint list | grep <pod-ip>

# 2. Policy hit
hubble observe --to-pod <ns>/<pod> --verdict DROPPED --since 5m

# 3. Service backend
kubectl get endpointslices -n <ns> -l kubernetes.io/service-name=<svc>

# 4. Agent logs
kubectl -n kube-system logs ds/cilium -c cilium-agent --tail=100
```

## Gotchas

> [!WARNING]
> **NetworkPolicy default allow** — K8s without NP = all pods talk. Adding first deny-all without allow rules = outage.

> [!WARNING]
> **Label typos in policy** — `app: api` vs `app: api` with trailing space in deployment — Hubble shows DROPPED with empty reply.

- **kube-proxy + Cilium LB both on** — double NAT weirdness; pick one mode per install guide.
- **MTU / overlay** — VXLAN overhead; need MSS clamp or jumbo path issues manifest as partial TCP.
- **Host firewall (ufw)** — blocks Geneve/VXLAN between nodes.
- **Cilium strict mode** — breaks legacy apps expecting arbitrary egress; roll out namespace by namespace.
- **L7 policy needs proxy** — first packet latency; ensure resources for Envoy sidecar path.

## When NOT to use

- **Tiny single-node lab** — flannel/canal simpler; Cilium shines at policy + observability scale.
- **Non-Kubernetes bare metal** — Cilium exists but different install; don't assume kube chart.
- **Replacing app auth with NP** — network segmentation complements, doesn't replace mTLS/authZ.

## Related

[[Kubernetes services]] [[ingress]] [[kubectl]] [[Pods]] [[Networking]]
