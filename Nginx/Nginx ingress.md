[[Configuration]] [[Kubernetes]] [[TLS (Transport Layer Security)]] [[certbot (letsencrypt)]]

# Nginx ingress

> Kubernetes Ingress controller built on Nginx — L7 HTTP(S) routing to Services by host and path, with TLS termination at the edge.

```txt
        Nginx ingress ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Cluster interviews ask Ingress vs Service vs Gateway API, why empty Endpoints…

## Sources
- [kubernetes/ingress-nginx docs](https://kubernetes.github.io/ingress-nginx/) — deep-dive
- [Kubernetes — Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) — overview
- [Kubernetes — Gateway API](https://gateway-api.sigs.k8s.io/) — overview

## Key Concepts
- **Ingress resource:** Declares host/path rules; the controller implements them.
- **TLS termination:** Certificates at the Ingress layer (often via cert-manager).
- **Host/path routing:** Route by hostname and URL path to backend Services.
- **Extras (controller-dependent):** Rate limiting, IP allowlists, custom errors, basic auth / OAuth2 / JWT integr…


- **Core:** Nginx Ingress is an Ingress controller: it watches Ingress (and related) obje…

## Technical Details
- Example Ingress (structure):

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: basic-ingress
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app
                port:
                  number: 80
```

```bash
kubectl get ingress -A
kubectl describe ingress my-app -n prod
helm upgrade ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx
```

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 from ingress | path rule; backend Service | `kubectl describe ingress`; check `pathType` |
| 502/503 | Endpoints empty; pod not ready | `kubectl get endpoints`; readiness probe |
| Certificate not issued | cert-manager issuer; challenge | `kubectl describe certificate` |
| Wrong host routed | Ingress class; duplicate ingress | Check `ingressClassName` and annotation precedence |

## Mistakes to Avoid
- **Mistake:** Expecting Ingress alone to serve traffic without a healthy Servi…
- **Mistake:** Forgetting `ingressClassName` when multiple controllers exist
- **Mistake:** Treating Ingress as a TCP/UDP proxy

## Pros/Cons or Trade-offs
- **Pro:** Familiar Nginx mental model inside Kubernetes; huge ecosystem of annotations.
- **Con:** Annotation sprawl and controller-specific behavior — not portable across Ingress implementations.
- **Con:** Classic Ingress is HTTP-centric; advanced traffic splitting often pushes teams toward Gateway API.

## Comparison
- vs host Nginx [[Configuration]]: CRD-driven and multi-tenant in-cluster vs static files on a VM.
- vs Gateway API: prefer Gateway API when you need richer, standardized traffic policies at scale.
- vs cloud LB only: Ingress adds L7 host/path routing inside the cluster.


### Use cases
- Expose a Deployment via Service + Ingress with TLS
