[[Docker]] [[Docker compose]] [[docker cli]] [[P2P (Peer-to-Peer)]]

# Swarm network

> Docker Swarm overlay network — multi-host virtual network so Swarm services reach each other by name across nodes (not BitTorrent “swarm”).

---

## Mental model

**Say it in one breath:** Swarm mode schedules services on a node cluster. **Overlay** networks encapsulate container traffic between hosts so `web` can resolve and dial `db` cluster-wide.

```txt
Node A (web task) ══overlay══ Node B (db task)
         DNS: db → task VIP / mesh
```

| Network type | Scope |
|--------------|--------|
| `bridge` | Single host |
| `overlay` | Multi-host Swarm |
| `host` / `ingress` | Special routing mesh / published ports |

(Name clash: Ethereum Swarm / BitTorrent “swarm” are unrelated P2P storage — different domain.)

---

## Standard config / commands

```bash
docker swarm init
docker network create -d overlay --attachable appnet
docker service create --name web --network appnet -p 80:80 nginx
docker service create --name api --network appnet myapi:1.0

docker network ls
docker service inspect web --pretty
```

| Knob | Why it matters |
|------|----------------|
| `--attachable` | Allow standalone containers to join overlay |
| Routing mesh | Published ports hit any node → VIP |
| Encryption `--opt encrypted` | Wire protection between nodes |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Service DNS not found | Same network? | Attach both services to overlay |
| Cross-node timeout | UDP 4789 / IP protocol 50 | Open overlay ports between nodes |
| Works on one node only | Tasks co-located by chance | Scale; check overlay; firewall |
| Ingress port dead | Mesh / VIP | `docker service ps`; republish port |
| “This node is not a swarm manager” | Worker context | Route manage commands to manager |

---

## Gotchas

> [!WARNING]
> **Swarm ≠ Kubernetes** — lighter, fewer features; many shops moved to K8s.

> [!WARNING]
> **Overlay needs open datapath** — cloud SGs often forget VXLAN ports.

> [!WARNING]
> **Routing mesh surprises** — traffic may enter a node with no local task.

---

## When NOT to use

- **Single-host compose** — bridge + [[Docker compose]] is enough.
- **Large multi-tenant production** — Kubernetes/ECS usually win.
- **Non-Docker P2P storage** — don’t confuse with BitTorrent/Ethereum Swarm.

---

## Related

[[Docker compose]] [[docker cli]] [[docker container]] [[P2P (Peer-to-Peer)]]
