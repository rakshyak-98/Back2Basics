<!-- note-strategy: operational -->
[[Kubernates]]

# Kubernetes services

> Kubernetes services — in Kubernetes, a service is a method for exposing a network application that is running as one or more Pods in your cluster.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Kubernetes services — in Kubernetes, a service is a method for exposing a network application that is running as one or more Pods in your cluster.

in Kubernetes, a service is a method for exposing a network application that is running as one or more [[Pods]] in your cluster.
A Service is an abstraction that defines a logical set of [[Pods]] and a policy to access them.
- It enables seamless communication between different parts of an application and external clients by providing a stable endpoint, even as the underlying Pods may change.
- Service decouple the frontend from backend Pods, ensuring consistent access despite Pod restarts or scaling operations
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
   app.kubernetes.io/name: MyApp
  ports:
   - port: 80
  # By default and for convenience, the `targetPort` is set to
  # the same value as the `port` field.
   targetPort: 80
   # Optional field
   # By default and for convenience, the Kubernetes control plane
   # will allocate a port from a range (default: 30000-32767)

## Standard config / commands

```bash
kubectl get svc -A
kubectl describe svc my-service
kubectl get endpoints my-service
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Service has no endpoints | selector mismatch; pods not ready | Labels on Pod template must match Service selector |
| ClusterIP works; NodePort does not | firewall; wrong nodePort | Open node port; curl node IP:port |
| DNS name does not resolve | CoreDNS down; wrong namespace | `kubectl -n kube-system get pods -l k8s-app=kube-dns` |
| External traffic not reaching pods | `externalTrafficPolicy: Local` | Check endpoints on node receiving traffic |

---

## Gotchas

> [!WARNING]
> A Service is a **stable virtual IP** — kube-proxy or dataplane programs rules to Pod IPs behind it.

---

## When NOT to use

- Do not use NodePort for production internet exposure — use LoadBalancer or Ingress.


---

## Related

[[Kubernates]]
