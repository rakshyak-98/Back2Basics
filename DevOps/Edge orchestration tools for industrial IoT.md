[[DevOps]] [[orchestration]] [[Docker]] [[Kubernetes]]

# Edge orchestration tools for industrial IoT

> Edge orchestration — deploy, update, and watch containerized workloads on factory/remote devices that often have weak WAN and must keep running offline.

---

## How it works

```txt
Cloud / hub control plane
        │ desired state, images, policies
        ▼
Edge site (kiosk/gateway) ── local apps ── machines/sensors
        │
        └── store-and-forward when WAN down
```

| Tool | Fit |
|------|-----|
| **KubeEdge** | K8s-native edge nodes |
| **K3s** | Light K8s for constrained sites |
| **ZEDEDA / EVE-OS** | Secure edge OS + app deploy |
| **Avassa** | Multi-site container orchestration / fleets |

---


## Configuration and commands

```bash
# K3s-shaped mental loop (illustrative)
curl -sfL https://get.k3s.io | sh -
kubectl apply -f edge-app.yaml
kubectl get nodes -o wide
```

| Knob | Why it matters |
|------|----------------|
| Image pre-cache | WAN too thin for pull-on-boot |
| Resource limits | Cameras/models starve PLC bridges |
| Signed artifacts | Untrusted remote sites |
| Dual-homing | OT vs IT networks isolation |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| App stuck `ImagePullBackOff` | WAN / registry | Mirror registry on-site; pre-load |
| Node NotReady after power blip | Disk / agent | Watchdog; durable containerd store |
| Config drift vs cloud | Agent sync lag | Force reconcile; conflict policy |
| OT traffic jitter | App CPU steal | cgroups/CPU pin; separate NICs |
| Update bricks site | No canary / rollback | Staged rollouts; last-good image pin |

---


## Gotchas

> [!WARNING]
> **Cloud-first assumptions fail offline** — every control action needs a local fallback.

> [!WARNING]
> **OT security zones** — don’t bridge plant floor to internet for convenience.

> [!WARNING]
> **Clock skew** — certs and TOTP-like device auth break without NTP/GPS discipline.

---


## When not to use

- **Single well-connected datacenter** — normal K8s/ECS is enough.
- **Tiny PLC ladder only** — classic OT tools, not container fleets.
- **Strict air gap with no update story** — orchestration without a secure sneakernet process is fantasy.

---


## Related

[[orchestration]] [[Docker]] [[ecommerce-cicd-environments]] [[HES Architecture]]

## Sources

- [Wikipedia — Edge orchestration tools for industrial IoT](https://en.wikipedia.org/wiki/Edge_orchestration_tools_for_industrial_IoT)
