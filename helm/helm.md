[[cli]] [[Kubernates/kubectl]] [[Kubernates/Pods]]

# Helm

> Kubernetes package manager — charts template manifests; releases track what you installed and how to upgrade or roll back.





## Interview Relevance
Interviewers distinguish chart/release/repo, templating (`values` → manifests), and hooks/CRDs as common footguns.

## Sources
- [Helm — Docs](https://helm.sh/docs/) — deep-dive
- [CNCF — Helm](https://www.cncf.io/projects/helm/) — overview

## Key Concepts
- **Templates:** Go templates render Kubernetes YAML.
- **Values:** configuration knobs; override per environment.
- **Release history:** revisions enable rollback.
- **CRDs / hooks:** charts may install custom resources or lifecycle jobs — read notes.

## Technical Details
```bash
helm list
helm get values my-release
helm install my-release bitnami/nginx
helm upgrade my-release bitnami/nginx -f values.yaml
helm rollback my-release 1
```

Charts can include many resource kinds (Deployments, Services, CRDs). The resource `kind` field is standard Kubernetes; Helm applies whatever the templates render.

```
Chart + values → rendered manifests → cluster objects (release)
```

## Real-World Applications
Standardize third-party stack installs (monitoring, ingress, databases operators) with pinned chart versions.

**Example:** Prod and staging share a chart with different `values-prod.yaml` / `values-staging.yaml`.

## Pros/Cons or Trade-offs
- **Pro:** Ecosystem + revisioned releases.
- **Con:** Abstraction hides YAML — always `helm template` before big upgrades.

## Comparison
- vs [[cli]]: conceptual model vs command cheat sheet.
- vs plain GitOps manifests: Helm adds packaging; GitOps still applies the output.

## Mistakes to Avoid
- Blind upgrades without rendering/diffing.
- Letting chart defaults open LoadBalancers in the wrong environment.
- Ignoring CRD upgrade instructions in chart docs.
