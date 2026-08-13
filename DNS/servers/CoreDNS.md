[[DNS server]] · [[Kubernates/kubectl]] · [[BIND]] · [[Unbound]]

# CoreDNS

> CoreDNS is a DNS server built as a chain of plugins — the default cluster DNS in Kubernetes, mapping `Service` and `Pod` names to cluster IPs with optional forwarding to upstream resolvers.

---

## Plugin model

Each request passes through configured plugins in `Corefile`:

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

## Kubernetes integration

- Service `kube-dns` or `coredns` in `kube-system`
- Pods use `/etc/resolv.conf` `nameserver 10.96.0.10` (cluster IP varies)
- **Stub domains** and **upstream nameservers** via ConfigMap `coredns` or `dns` config

```bash
kubectl -n kube-system get configmap coredns -o yaml
kubectl -n kube-system logs -l k8s-app=kube-dns
```

## Debugging cluster DNS

```bash
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default
dig @10.96.0.10 my-svc.my-ns.svc.cluster.local
```

Failures often trace to **NetworkPolicy**, **CoreDNS pod not ready**, or **forward plugin** unable to reach corporate resolver.

## vs [[BIND]] / [[Unbound]]

CoreDNS targets **dynamic service discovery** with a small footprint. BIND/Unbound suit Internet zones and validating recursion.

## Recall

- What plugin answers `*.svc.cluster.local` names?
- Where do Pods get their nameserver IP in Kubernetes?

## Sources

- [CoreDNS documentation](https://coredns.io/manual/toc/)
- [Kubernetes DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
