[[orchestration]] [[Docker]] [[Pods]] [[ecommerce-cicd-environments]] [[HES Architecture]]

# Edge orchestration tools for industrial IoT

> Deploy, update, and watch container workloads on factory or remote devices that often have weak WAN links and must keep running offline.

```txt
        Edge orchestration ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about edge orchestration to see whether you understand cloud…

## Sources
- [KubeEdge documentation](https://kubeedge.io/docs/) — overview
- [K3s documentation](https://docs.k3s.io/) — overview
- [CNCF — KubeEdge](https://www.cncf.io/projects/kubeedge/) — overview

## Key Concepts
- **Cloud/hub control plane:** desired state, images, and policies → operators manage fleets from one place.
- **Edge autonomy:** local runtime keeps workloads up when WAN drops → store-and-forward sync late…
- **Image pre-cache:** pull-on-boot fails on thin links → mirror or preload images on site.
- **OT vs IT isolation:** plant-floor networks stay separated → dual-homing and signed artifacts matter.
- **Tool fit:** KubeEdge (Kubernetes-native edge), K3s (light cluster), ZEDEDA/EVE-OS (secure…


- **Core:** Edge orchestration is the control plane and local runtime that keep desired-s…

## Technical Details
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
| **KubeEdge** | Kubernetes-native edge nodes with cloud–edge sync |
| **K3s** | Lightweight Kubernetes for constrained sites |
| **ZEDEDA / EVE-OS** | Secure edge OS plus application deploy |
| **Avassa** | Multi-site container orchestration / fleets |

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
| Dual-homing | OT vs IT network isolation |

| Symptom | Check | Fix |
|---------|-------|-----|
| App stuck `ImagePullBackOff` | WAN / registry | Mirror registry on-site; pre-load |
| Node NotReady after power blip | Disk / agent | Watchdog; durable containerd store |
| Configuration drift vs cloud | Agent sync lag | Force reconcile; conflict policy |
| OT traffic jitter | App CPU steal | cgroups/CPU pin; separate NICs |
| Update bricks site | No canary / rollback | Staged rollouts; last-good image pin |

## Mistakes to Avoid
- **Mistake:** Assuming cloud-first pull-and-run works offline
- **Mistake:** Bridging plant-floor OT networks to the internet for convenience
- **Mistake:** Ignoring clock skew
- **Mistake:** Treating air-gapped sites as orchestratable without a secure sne…

## Pros/Cons or Trade-offs
- **Pro:** One operational model for many remote sites with offline survival.
- **Con:** Harder debugging than a single datacenter cluster — clocks, certs, and sync lag dominate.
- **Con:** Overkill for one well-connected site or pure ladder-logic PLC work.

## Comparison
- vs datacenter [[orchestration]] / full Kubernetes: edge tools assume intermittent WAN and local a…
- vs single-node [[Docker]]: Docker alone lacks fleet desired-state, signed rollout, and multi-site…


### Use cases
- Factories run vision models and PLC bridges on gateways that lose internet fo…

- **Example:** A plant gateway hits `ImagePullBackOff` after a reboot because t…
