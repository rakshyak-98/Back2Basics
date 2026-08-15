[[DNS server]] [[Kubernates/kubectl]] [[BIND]] [[Unbound]] [[name server]]

# CoreDNS

> CoreDNS is a DNS server built as a chain of plugins — the default cluster DNS in Kubernetes, mapping `Service` and `Pod` names to cluster IPs with optional forwarding to upstream resolvers.

## Interview Relevance

Kubernetes interviews ask how `svc.namespace.svc.cluster.local` resolves, where the Corefile lives, and how forward/cache plugins affect external lookups.

## Sources

- [CoreDNS documentation](https://coredns.io/manual/toc/) — deep-dive
- [Kubernetes DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) — deep-dive

## Key Concepts

- **Plugin chain:** each query walks ordered plugins in the Corefile.
- **kubernetes plugin:** answers Service/Pod names in `cluster.local`.
- **forward + cache:** external names go upstream with TTL-aware caching.
- **Cluster wiring:** Pods get `nameserver` pointing at the `kube-dns`/`coredns` Service.

## Technical Details

```
.:53 {
    errors
    health
    kubernetes cluster.local in-addr.arpa ip6.arpa {
        pods insecure
        fallthrough in-addr.arpa ip6.arpa
    }
    prometheus :9153
    forward . /etc/resolv.conf
    cache 30
    loop
    reload
    loadbalance
}
```

| Plugin | Role |
|--------|------|
| `kubernetes` | Answers `svc.namespace.svc.cluster.local` |
| `forward` | Upstream for external names |
| `cache` | TTL-aware caching |
| `hosts` | Static overrides like `/etc/hosts` |
| `rewrite` | Modify queries/responses |
| `etcd` / `file` | Alternative backends |

**Kubernetes integration**

- Service `kube-dns` or `coredns` in `kube-system`
- Pods use `/etc/resolv.conf` `nameserver 10.96.0.10` (cluster IP varies)
- **Stub domains** and **upstream nameservers** via ConfigMap `coredns` or `dns` config

```bash
kubectl -n kube-system get configmap coredns -o yaml
kubectl -n kube-system logs -l k8s-app=kube-dns
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default
dig @10.96.0.10 my-svc.my-ns.svc.cluster.local
```

Failures often trace to **NetworkPolicy**, **CoreDNS pod not ready**, or **forward plugin** unable to reach corporate resolver.

## Real-World Applications

In-cluster service discovery; stub-domain forwarding to on-prem DNS for hybrid names.

**Example:** `my-api.default.svc.cluster.local` resolves via CoreDNS; `api.corp.example` falls through `forward` to the office recursive resolver.

## Pros/Cons or Trade-offs

- **Pro:** Small footprint, plugin model, first-class Kubernetes integration.
- **Con:** Not a replacement for Internet authoritative zone masters ([[BIND]] / PowerDNS).
- **Con:** Misconfigured `forward` or NetworkPolicy makes “DNS is down” for the whole cluster.

## Comparison

- vs [[BIND]] / [[Unbound]]: CoreDNS targets dynamic service discovery; BIND/Unbound suit Internet zones and validating recursion.
- vs [[dnsmasq]]: dnsmasq is LAN/DHCP edge; CoreDNS is cluster DNS.

## Mistakes to Avoid

- Editing the wrong ConfigMap or forgetting CoreDNS pods reload after Corefile changes.
- Blocking CoreDNS with NetworkPolicy while debugging “service DNS failed.”
- Expecting CoreDNS alone to host public Internet zones with full DNSSEC zone-master workflows.
