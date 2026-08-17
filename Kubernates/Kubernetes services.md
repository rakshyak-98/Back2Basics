[[Pods]] [[ingress]] [[kubectl]] [[Cilium]]

# Kubernetes services

> A Service is a stable virtual IP and DNS name in front of a changing set of Pods — kube-proxy or the CNI dataplane load-balances to ready endpoints.

```txt
        Kubernetes service ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers test Service types, selector/endpoint mismatch, and when to use …

## Sources
- [Kubernetes — Service](https://kubernetes.io/docs/concepts/services-networking/service/) — deep-dive
- [Kubernetes — DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) — overview

## Key Concepts
- **Stable front door:** Pods come and go; Service IP/DNS stays.
- **Selector → Endpoints/EndpointSlices:** only Ready pods matching labels receive traffic.
- **Types:** ClusterIP (in-cluster), NodePort (node ports), LoadBalancer (cloud LB), Exter…
- **DNS:** `http://<svc>.<ns>.svc.cluster.local:<port>` — not `localhost` across pods.

## Technical Details
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
      targetPort: 80
```

```bash
kubectl get svc -A
kubectl describe svc my-service
kubectl get endpoints my-service
kubectl get endpointslices -l kubernetes.io/service-name=my-service
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Service has no endpoints | selector mismatch; pods not ready | Labels on Pod template must match Service selector |
| ClusterIP works; NodePort does not | firewall; wrong nodePort | Open node port; curl node IP:port |
| DNS name does not resolve | CoreDNS down; wrong namespace | `kubectl -n kube-system get pods -l k8s-app=kube-dns` |
| External traffic not reaching pods | `externalTrafficPolicy: Local` | Check endpoints on node receiving traffic |

## Mistakes to Avoid
- **Mistake:** Mismatched labels between Deployment template and Service select…
- **Mistake:** Using NodePort as the primary production internet exposure
- **Mistake:** Expecting `localhost` in pod A to reach service B
- **Mistake:** Ignoring readiness

## Pros/Cons or Trade-offs
- **Pro:** Decouples clients from Pod IPs and enables rolling updates.
- **Con:** NodePort for public internet is awkward — prefer LoadBalancer or Ingress.
- **Con:** `externalTrafficPolicy: Local` can blackhole traffic on nodes without local pods.

## Comparison
- vs [[ingress]]: Service is L4 stable VIP; Ingress adds L7 host/path/TLS at the edge.
- vs direct Pod IP: Pod IPs are ephemeral — never hard-code them in clients.
- Dataplane policy → [[Cilium]].


### Use cases
- East-west microservice calls via ClusterIP DNS, cloud LoadBalancer for a sing…

- **Example:** Frontend pods call `http://api.prod.svc.cluster.local:80`
