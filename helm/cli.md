[[helm]] [[Kubernates/kubectl]] [[Kubernates/Kubernetes config]]

# Helm CLI

> Package manager commands for Kubernetes — add repos, install/upgrade releases, diff values, and rollback when a chart deploy goes wrong.

```txt
        Helm CLI ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want release vs chart, `values.yaml` overrides, upgrade/rollback…

## Sources
- [Helm — Commands](https://helm.sh/docs/helm/) — deep-dive
- [Helm — Values files](https://helm.sh/docs/chart_template_guide/values_files/) — overview

## Key Concepts
- **Chart:** packaged templates + default values.
- **Release:** installed instance of a chart with a name.
- **Repo:** chart museum/HTTP index (`helm repo add`).
- **Overrides:** `-f values.yaml` / `--set` for environment differences.

## Technical Details
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install my-release bitnami/nginx -f values.yaml
helm upgrade my-release bitnami/nginx -f values.yaml
helm rollback my-release 1
helm list
helm get values my-release
helm uninstall my-release
```

| Task | Command |
|------|---------|
| Add repo | `helm repo add <name> <url>` |
| Install | `helm install <release> <chart>` |
| Upgrade | `helm upgrade <release> <chart>` |
| Rollback | `helm rollback <release> <revision>` |

## Mistakes to Avoid
- **Mistake:** `--set` sprawl unreviewed in CI
- **Mistake:** Upgrading without checking `helm get values` drift
- **Mistake:** Assuming chart `kind` quirks without reading CRD notes in the ch…

## Pros/Cons or Trade-offs
- **Pro:** Repeatable installs; rich ecosystem charts.
- **Con:** Templating complexity and surprise defaults if you do not read values.

## Comparison
- vs raw `kubectl apply`: Helm tracks revisions and packages.
- vs Kustomize: Helm packages params; Kustomize overlays plain manifests.


### Use cases
- Deploy ingress-nginx or a third-party operator with env-specific values per c…

- **Example:** Bad image tag
