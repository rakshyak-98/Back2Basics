[[Nginx]]

# Nginx ingress

> Nginx ingress — acts as a load balancer and Reverse Proxy for kubernetes cluster.

## Mental model

**Say it in one breath:** Nginx ingress — acts as a load balancer and Reverse Proxy for kubernetes cluster.

Acts as a load balancer and [[Reverse Proxy]] for kubernetes cluster.
Nginx ingress is a ingress controller for Kubernetes that manages external access to services running in a kubernetes cluster.
- enables secure and scalable HTTP(S) traffic routing to Kubernetes workloads.
- rate limiting, IP whitelisting, and custom error page.
Load Balancing: Distributes traffic across multiple back-end pods to ensure reliability and scalability
SSL/TLS Termination: Handles HTTPS traffic by terminating SSL connections at the ingress layer.
Host-Based Routing: Routes requests based on URL paths or hostnames.
Authentication: Supports basic authentication, JWT, and OAuth2 integration.
### Example nginx ingress config file
```yaml
apiVersion: networking.k8s.io/v1 # must be appropriate version
kind: Ingress # Always set to Ingress
metadata:
	name: basic-ingress # Name of the ingress resource
spec:
	rules: # specifies at leat one routing rule (host and path)

## Standard config / commands

```bash
kubectl get ingress -A
kubectl describe ingress my-app -n prod
helm upgrade ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| 404 from ingress | path rule; backend Service | `kubectl describe ingress`; check `pathType` |
| 502/503 | Endpoints empty; pod not ready | `kubectl get endpoints`; readiness probe |
| Certificate not issued | cert-manager issuer; challenge | `kubectl describe certificate` |
| Wrong host routed | Ingress class; duplicate ingress | Check `ingressClassName` and annotation precedence |

## Gotchas

> [!WARNING]
> Ingress only routes HTTP — you still need a **Service** with healthy Endpoints behind it.

## When NOT to use

- Use Gateway API instead of Ingress when you need advanced traffic splitting at scale.

## Related

[[Nginx]]
