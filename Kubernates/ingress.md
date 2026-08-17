[[Kubernetes services]] [[kubectl]] [[Cilium]] [[Nginx Configuration]] [[certbot]]

# ingress

> Ingress routes HTTP(S) from the internet to Services by host and path — but only after an Ingress Controller is installed to watch Ingress objects and program the data plane.

```txt
        ingress ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers separate Ingress YAML from the controller, expect TLS + IngressC…

## Sources
- [Kubernetes — Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) — deep-dive
- [ingress-nginx documentation](https://kubernetes.github.io/ingress-nginx/) — overview
- [Gateway API](https://gateway-api.sigs.k8s.io/) — overview

## Key Concepts
- **Two objects:** `Ingress` (rules you write) versus Ingress Controller (Deployment that config…
- **Ingress alone does nothing:** without a matching `ingressClassName`.
- **Path:** Internet → LB/NodePort → controller → TLS/host/path → Service → Pod endpoints.
- **Gateway API:** is the successor spec; Ingress remains widely deployed.

## Technical Details
```
Internet ──► LB / NodePort ──► Ingress Controller
                                      │
                                      ├── TLS termination
                                      ├── host/path routing
                                      └── backend Service:port
```

| Controller | Typical use |
|------------|-------------|
| **ingress-nginx** | General self-hosted; annotations rich |
| **Traefik** | Docker-native shops; auto-discovery |
| **AWS LB Controller** | EKS → ALB/NLB |
| **GCE / GKE Ingress** | GCP integrated |
| **Cilium Ingress** | eBPF + policy unified — [[Cilium]] |
| **Gateway API** | Successor spec |

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  namespace: prod
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts: [api.example.com]
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 80
```

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace
kubectl get ingressclass
kubectl get ingress -n prod
kubectl describe ingress -n prod api
kubectl get endpointslices -n prod -l kubernetes.io/service-name=api
kubectl logs -n ingress-nginx deploy/ingress-nginx-controller --tail=50
```

### 502 vs 503

```
502: Client → Controller OK → backend connection refused/timeout/reset
503: Client → Controller → no healthy endpoints (readiness / empty Endpoints)
```

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 from ingress | host/path rule mismatch | Add rule; check `pathType` Prefix vs Exact |
| 503 Service Unavailable | endpoints empty | Fix readiness; pod crash |
| 502 intermittent | controller + app logs | Timeouts; pod restarts; HPA flapping |
| 525/526 SSL | origin cert | Full chain in secret; SNI host match |
| Wrong backend | multiple Ingress same host | Rule precedence; merge order |
| Works via port-forward, not ingress | Service selector | Labels; different namespace |
| Infinite redirect | http→https loop | `ssl-redirect` + backend HTTP scheme |

- Playbook: describe ingress → endpoints → pods Ready → app logs → controller l…

## Mistakes to Avoid
- **Mistake:** Creating Ingress without IngressClass
- **Mistake:** Stopping at a green cert when 502 means the backend is still bro…
- **Mistake:** `targetPort` ≠ `containerPort`; app bound to `127.0.0.1` only
- **Mistake:** Large uploads without `proxy-body-size`

## Pros/Cons or Trade-offs
- **Pro:** One edge for many HTTP Services with host/path/TLS.
- **Con:** Controller outage is shared blast radius — run ≥2 replicas + PDB.
- **Con:** Non-HTTP TCP needs LoadBalancer or Gateway TCPRoute, not classic Ingress.

## Comparison
- vs ClusterIP alone: Ingress is for north-south HTTP; east-west stays on Service DNS.
- vs mesh mTLS: mesh secures east-west; public clients still need edge TLS termination.
- vs Gateway API: prefer platform guidance on new clusters.


### Use cases
- Public API hostnames with TLS (cert-manager), path-based routing to multiple …

- **Example:** `api.example.com` TLS terminates at nginx
