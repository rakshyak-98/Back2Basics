[[Kubernetes services]] [[kubectl]] [[Cilium]] [[Nginx Configuration]]

# ingress

> HTTP/S routing into the cluster — **Ingress** = rules; **Ingress Controller** = program that implements them — **Kubernetes: Up and Running** (Burns et al.).

## Mental model

```
Internet ──► LB / NodePort ──► Ingress Controller (nginx, traefik, cilium, ALB…)
                                      │
                                      ├── TLS termination
                                      ├── host/path routing
                                      └── backend Service:port
```

**Ingress resource alone does nothing** — you must install a controller Deployment + class.

```
Ingress spec.rules[].host + path  ──maps──►  Service.name:port  ──►  Pod endpoints
```

Two objects, easy to confuse:

| Object | What it is |
|--------|------------|
| `Ingress` | Declarative routing rules (YAML you write) |
| Ingress Controller | Watches Ingress; configures data plane (nginx, Envoy, …) |

### Controller landscape

| Controller | Typical use |
|------------|-------------|
| **ingress-nginx** | General self-hosted; annotations rich |
| **Traefik** | Docker-native shops; auto-discovery |
| **AWS LB Controller** | EKS → ALB/NLB |
| **GCE / GKE Ingress** | GCP integrated |
| **Cilium Ingress** | eBPF + policy unified — see [[Cilium]] |
| **Gateway API** | Successor spec; Ingress still dominant |

```bash
kubectl get ingressclass
# ingress.spec.ingressClassName must match installed controller
```

## Standard config / commands

### Minimal Ingress + TLS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  namespace: prod
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod   # if using cert-manager
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
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

```yaml
# Backend must exist and pass readiness
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: prod
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 8080
```

### Install ingress-nginx (common pattern)

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace
kubectl get svc -n ingress-nginx   # EXTERNAL-IP or LoadBalancer hostname
```

### Verify path end-to-end

```bash
kubectl get ingress -n prod
kubectl describe ingress -n prod api
kubectl get endpointslices -n prod -l kubernetes.io/service-name=api

# From inside cluster
kubectl run curl --rm -it --image=curlimages/curl -- \
  curl -v -H 'Host: api.example.com' http://ingress-nginx-controller.ingress-nginx.svc/

# Controller logs
kubectl logs -n ingress-nginx deploy/ingress-nginx-controller --tail=50
```

## 502 / 503 debugging playbook

**502 Bad Gateway** — controller reached backend; backend returned garbage or connection failed.

```
502 path:
  Client → Controller OK → backend connection/refused/timeout/reset
503 path:
  Client → Controller → no healthy endpoints (readiness / empty Endpoints)
```

| Step | Command | Interpret |
|------|---------|-----------|
| 1 | `kubectl describe ingress -n prod` | Address assigned? Backend service name/port correct? |
| 2 | `kubectl get endpoints -n prod api` | Empty = no ready pods |
| 3 | `kubectl get pods -n prod -l app=api` | Running + Ready? |
| 4 | `kubectl logs -n prod -l app=api` | App listening on `targetPort`? |
| 5 | Controller logs | `connect() failed`, upstream timeout |
| 6 | Direct pod curl | `kubectl exec … curl localhost:8080/health` |
| 7 | NetworkPolicy | [[Cilium]] Hubble DROPPED to pod IP |

**Common root causes:**

- Service `targetPort` ≠ container `containerPort` (8080 vs 80).
- App binds `127.0.0.1` only — not reachable from controller pod network.
- Readiness probe passes localhost but app broken on real traffic path.
- TLS secret missing/wrong → 502 on HTTPS, HTTP works.
- Annotation typo (`nginx.ingress.kubernetes.io/backend-protocol: HTTPS` when app is HTTP).
- Timeout too low — long requests → 502 at 60s default.

```bash
# nginx ingress upstream debug annotation (temporary)
metadata:
  annotations:
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "5"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "120"
```

## Triage table

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 from ingress | host/path rule mismatch | Add rule; check `pathType` Prefix vs Exact |
| 503 Service Unavailable | endpoints empty | Fix readiness; pod crash — [[kubectl]] CrashLoop |
| 502 intermittent | controller + app logs | Timeouts; pod restarts; HPA flapping |
| 525/526 SSL (CF) | origin cert | Full chain in secret `tls.crt`; SNI host match |
| Wrong backend | multiple Ingress same host | Rule precedence; merge order |
| Works via port-forward, not ingress | Service selector | Labels; different namespace |
| Infinite redirect | http→https loop | `ssl-redirect` + backend HTTP scheme |

## Gotchas

> [!WARNING]
> **Ingress without IngressClass** — ignored on 1.18+ clusters; silent "nothing happens."

> [!WARNING]
> **cert-manager succeeded but 502** — TLS terminates at ingress; backend still broken — don't stop at green cert.

- **One LoadBalancer for many Ingress** — cost win; blast radius on controller outage — run ≥2 replicas + PDB.
- **Large upload 413** — `proxy-body-size` annotation.
- **WebSocket** — needs `Upgrade` headers; some controllers need explicit annotation.
- **External DNS lag** — Ingress has ADDRESS but DNS not propagated.
- **Gateway API migration** — new clusters may skip Ingress; check platform docs.

## When NOT to use

- **Non-HTTP TCP services** — use `Service type=LoadBalancer` or Gateway API TCPRoute.
- **Internal-only east-west** — ClusterIP Service directly; no ingress hop.
- **Mesh mTLS replaces ingress TLS** — still need edge termination for public clients.

## Related

[[Kubernetes services]] [[kubectl]] [[Cilium]] [[Nginx Configuration]] [[certbot]]
