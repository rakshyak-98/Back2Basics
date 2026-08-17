[[Docker compose]] [[docker cli]] [[docker container]] [[P2P (Peer-to-Peer)]]

# Swarm network

> Docker Swarm overlay networking — a multi-host virtual network so Swarm services reach each other by name across nodes (not BitTorrent or Ethereum “swarm”).





## Interview Relevance
Interviewers use Swarm networking to check overlay versus bridge, routing mesh surprises, and whether you know when Swarm is enough versus Kubernetes.

## Sources
- [Docker — Swarm networking](https://docs.docker.com/engine/swarm/networking/) — deep-dive
- [Docker — Overlay network driver](https://docs.docker.com/network/drivers/overlay/) — overview

## Key Concepts
- **Overlay scope:** VXLAN-backed fabric so tasks on different nodes share DNS and service VIPs.
- **Bridge vs overlay:** `bridge` is single-host; `overlay` is multi-host Swarm; `host` / `ingress` handle published ports and routing mesh.
- **Routing mesh:** published ports can hit any node and forward to the service VIP — traffic may enter a node with no local task.
- **Name clash:** Ethereum Swarm / BitTorrent “swarm” are unrelated P2P storage domains.

## Technical Details
```txt
Node A (web task) ══overlay══ Node B (db task)
         DNS: db → task VIP / mesh
```

| Network type | Scope |
|--------------|--------|
| `bridge` | Single host |
| `overlay` | Multi-host Swarm |
| `host` / `ingress` | Special routing mesh / published ports |

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

| Symptom | Check | Fix |
|---------|-------|-----|
| Service DNS not found | Same network? | Attach both services to overlay |
| Cross-node timeout | UDP 4789 / IP protocol 50 | Open overlay ports between nodes |
| Works on one node only | Tasks co-located by chance | Scale; check overlay; firewall |
| Ingress port dead | Mesh / VIP | `docker service ps`; republish port |
| “This node is not a swarm manager” | Worker context | Route manage commands to manager |

## Real-World Applications
Small Docker-native clusters that need service discovery across a few VMs without running full Kubernetes.

**Example:** `web` and `api` services join `appnet`; clients hit any node on port 80 and the ingress mesh routes to a `web` task.

## Pros/Cons or Trade-offs
- **Pro:** Lightweight multi-host networking with built-in DNS and mesh — less moving parts than a full CNI stack.
- **Con:** Swarm is feature-light versus Kubernetes; many shops have migrated.
- **Con:** Overlay datapath needs open VXLAN / ESP ports — cloud security groups often omit them.

## Comparison
- vs single-host [[Docker compose]]: bridge + Compose is enough on one Engine.
- vs Kubernetes CNI ([[Cilium]], Calico): K8s wins for large multi-tenant production and NetworkPolicy depth.
- vs [[P2P (Peer-to-Peer)]] swarms: different domain — do not confuse names.

## Mistakes to Avoid
- Assuming Swarm equals Kubernetes capability for HA, PDBs, and policy.
- Forgetting overlay firewall rules between nodes.
- Surprising operators with routing mesh — traffic enters nodes that hold no task.
- Managing Swarm from a worker instead of a manager.
