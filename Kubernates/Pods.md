[[kubectl]] [[kubectl pod creation]] [[Kubernetes services]] [[ingress]]

# Pods

> A Pod is the smallest schedulable unit in Kubernetes — one or more containers that share network namespace and volumes on one node.

```txt
        Pods ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers check that you know Pods are ephemeral (new IP on restart), why …

## Sources
- [Kubernetes — Pods](https://kubernetes.io/docs/concepts/workloads/pods/) — deep-dive
- Brendan Burns et al., *Kubernetes: Up and Running* — overview

## Key Concepts
- **Shared fate:** containers in a Pod share IP, localhost, and optional volumes.
- **Ephemeral identity:** restart/reschedule creates a new Pod object/IP unless a controller recreates …
- **Controllers own resilience:** Deployment/StatefulSet/Job recreate Pods; bare Pods do not survive node loss.
- **Probes:** readiness controls Service membership; liveness restarts stuck containers.

## Technical Details
```bash
kubectl get pods -A -o wide
kubectl describe pod my-pod -n default
kubectl logs my-pod -c app
kubectl delete pod my-pod --grace-period=0 --force   # last resort
```

| Symptom | Check | Fix |
|---------|-------|-----|
| CrashLoopBackOff | `kubectl logs --previous`; probe failures | Fix exit code; adjust command or probes |
| ImagePullBackOff | image name; pull secret | `kubectl describe pod`; fix registry auth |
| Pending | CPU/memory; PVC bind | `kubectl describe node`; check requests and storage class |
| Running but not Ready | readiness probe failing | Hit probe path from inside cluster |

- One main process per container
- Creation paths → [[kubectl pod creation]].

## Mistakes to Avoid
- **Mistake:** Running production apps as bare Pods
- **Mistake:** Putting multiple unrelated main processes in one container
- **Mistake:** Assuming Pod IP stays stable across restarts
- **Mistake:** Force-deleting without understanding controller recreation

## Pros/Cons or Trade-offs
- **Pro:** Dense packing and co-located sidecars with shared localhost.
- **Con:** No self-healing without a controller.
- **Con:** In-memory state dies with the Pod — persist to volumes or external stores.

## Comparison
- vs container: Pod is the Kubernetes API object; one or more containers inside.
- vs Deployment: Deployment owns replica count and rolling updates of Pod templates.
- Networking exposure → [[Kubernetes services]] · [[ingress]].


### Use cases
- Application replicas behind a Service, debug shells (`netshoot`), and init co…

- **Example:** An API Pod fails readiness → removed from Endpoints → [[ingress]…
