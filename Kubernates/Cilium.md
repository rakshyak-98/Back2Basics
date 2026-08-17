[[Kubernetes services]] [[ingress]] [[kubectl]] [[Pods]]

# Cilium

> Cilium is an eBPF-powered CNI — pod networking, optional kube-proxy replacement, NetworkPolicy (including L7), and Hubble flow observability.

```txt
        Cilium ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask why eBPF beats iptables at scale, how identity is label-base…

## Sources
- [Cilium documentation](https://docs.cilium.io/) — deep-dive
- [Cilium — Network Policy](https://docs.cilium.io/en/stable/security/policy/) — overview
- Brendan Burns et al., *Kubernetes: Up and Running* — overview

## Key Concepts
- **eBPF dataplane:** filter/NAT/route in-kernel without iptables chain explosion at large Service …
- **Identity = labels:** policies survive Pod IP changes.
- **Components:** cilium-agent (per node), cilium-operator, Hubble relay/UI, optional Envoy for…
- **kube-proxy replacement:** BPF service LB maps — do not run both modes blindly.

## Technical Details
```
Pod eth0 ──► veth ──► node eBPF (Cilium) ──► cluster routing / encap
                           │
                           ├── NetworkPolicy (L3/L4/L7)
                           ├── Service load-balancing
                           └── Hubble: flow logs + metrics
```

```bash
kubectl -n kube-system get pods -l k8s-app=cilium
cilium status --wait
kubectl -n kube-system exec ds/cilium -- cilium status
kubectl -n kube-system exec ds/cilium -- cilium service list

hubble observe --namespace prod --pod api-
hubble observe --protocol tcp --port 5432 --verdict DROPPED
hubble observe --from-label app=frontend --to-label app=api --follow
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-ingress
  namespace: prod
spec:
  podSelector:
    matchLabels: { app: api }
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels: { app: frontend }
      ports:
        - protocol: TCP
          port: 8080
```

- CiliumNetworkPolicy adds DNS-aware/L7 HTTP rules when standard NetworkPolicy …

- Debug flow:

```bash
kubectl -n kube-system exec ds/cilium -- cilium endpoint list | grep <pod-ip>
hubble observe --to-pod <ns>/<pod> --verdict DROPPED --since 5m
kubectl get endpointslices -n <ns> -l kubernetes.io/service-name=<svc>
kubectl -n kube-system logs ds/cilium -c cilium-agent --tail=100
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Pod `ContainerCreating` stuck | describe; Cilium IPAM events | Free CIDR; fix IPAM; restart agent |
| Service unreachable | `cilium service list`; endpoints | Missing backends; BPF LB disabled |
| Policy suddenly blocks traffic | `hubble observe --verdict DROPPED` | Label mismatch; add explicit allow |
| DNS timeouts | Hubble to kube-dns; CoreDNS policy | Allow udp/53 to kube-system |
| NodeNotReady after upgrade | `cilium status`; kernel | Match version matrix; eBPF modules |
| Cross-node pod fail | VXLAN/GENEVE vs routing | Fix underlay MTU / L2 adjacency |
| High CPU on cilium-agent | Map pressure, policy count | Split policies; reduce L7 scope |

## Mistakes to Avoid
- **Mistake:** First deny-all NetworkPolicy without allows
- **Mistake:** Running kube-proxy and Cilium BPF LB together incorrectly
- **Mistake:** Host firewall blocking Geneve/VXLAN between nodes
- **Mistake:** Label typos that Hubble shows as DROPPED with empty peers
- **Mistake:** Rolling strict mode cluster-wide instead of namespace by namespa…

## Pros/Cons or Trade-offs
- **Pro:** Unified networking, policy, and observability with strong scale characteristics.
- **Con:** Tiny single-node labs may prefer simpler CNIs; Cilium shines with policy + Hubble needs.
- **Con:** L7 policy adds proxy latency/resources; NetworkPolicy is not application authZ.

## Comparison
- vs flannel/canal: simpler overlay; less policy/observability depth.
- vs [[ingress]]: Cilium can also do Ingress; classic ingress-nginx still common at the edge.
- Complements mTLS/authZ — does not replace them.


### Use cases
- Zero-trust namespace policies, replacing kube-proxy at scale, and incident “w…

- **Example:** Frontend→API suddenly fails
