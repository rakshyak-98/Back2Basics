<!-- note-strategy: operational -->
[[DNS]] [[DNS server]] [[Unbound]] [[Pods]]

# CoreDNS

> CoreDNS — plugin-chained DNS server in Go; default cluster DNS in Kubernetes — forward, cache, kubernetes, rewrite by stacking plugins.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** A query walks a **Corefile** plugin chain — e.g. kubernetes → rewrite → cache → forward — until something writes an answer. In Kubernetes it maps Service/Pod names to ClusterIPs.

```txt
Query → errors → health → ready → kubernetes → forward → cache → loop → reload → loadbalance
                 (typical K8s Corefile order varies by chart)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Corefile** | Config: zones + plugin list | “DNS behavior is the plugin chain.” |
| **kubernetes plugin** | Watches API for Services/Endpoints | “svc.cluster.local comes from here.” |
| **forward** | Send upstream (node DNS / 8.8.8.8) | “Cluster DNS forwards external names.” |
| **rewrite** | Mutate question/answer | “Fix legacy names without changing apps.” |
| **stub domain** | Forward only some zones | “Corp DNS for `*.corp` via forward.” |

---

## Standard config / commands

```txt
# Corefile sketch (standalone forwarder + cache)
.:53 {
    forward . 1.1.1.1 8.8.8.8
    cache 30
    log
    errors
}
```

```bash
# Kubernetes
kubectl -n kube-system get cm coredns -o yaml
kubectl -n kube-system logs -l k8s-app=kube-dns
kubectl -n kube-system rollout restart deploy/coredns

# From a debug pod
nslookup kubernetes.default
dig @10.96.0.10 google.com   # cluster DNS ClusterIP
```

| Knob | Why it matters |
|------|----------------|
| `forward` targets | Node `/etc/resolv.conf` loops are common |
| `cache` TTL | Stale Service IPs after change vs query load |
| Autopath / ndots | Pods with `ndots:5` explode search-list queries |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Pods can’t resolve Services | CoreDNS pods Ready? | Fix CrashLoop; check Corefile syntax |
| External names fail | `forward` / network policy | Fix upstream; allow UDP/TCP 53 egress |
| `i/o timeout` to CoreDNS | CNI / kube-proxy / ClusterIP | Fix networking; test from same node |
| CPU spike | ndots + search domains | Lower `ndots`; enable cache; autopath carefully |
| SERVFAIL after edit | Bad Corefile | `coredns -conf Corefile` validate; rollback CM |
| Stale endpoint IP | Cache / endpoint slice lag | Wait/shorten cache; check Endpoints |

---

## Gotchas

> [!WARNING]
> **forward to 127.0.0.1 on the node** — easy to create a resolution loop with systemd-resolved.

> [!WARNING]
> **All DNS in the cluster shares one blast radius** — CoreDNS down → Services “disappear” by name.

> [!WARNING]
> **Plugin order matters** — cache before kubernetes (wrong order) serves ghosts; read the chain top to bottom.

---

## When NOT to use

- **Public authoritative hosting for customer domains** — [[BIND]] / PowerDNS ([[PoserDNS]]) fit better.
- **Heavy recursive with DNSSEC validation as an ISP** — [[Unbound]].
- **Home router all-in-one DHCP+DNS** — [[dnsmasq]].

---

## Related

[[DNS]] [[DNS server]] [[name server]] [[Unbound]] [[dnsmasq]] [[PoserDNS]] [[BIND]] [[Pods]]
