[[helm]] [[Kubernates/kubectl]] [[Kubernates/Kubernetes config]]

# Helm CLI

> Package manager commands for Kubernetes — add repos, install/upgrade releases, diff values, and rollback when a chart deploy goes wrong.

## Interview Relevance

Interviewers want release vs chart, `values.yaml` overrides, upgrade/rollback, and three-way merge awareness.

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

## Real-World Applications

Deploy ingress-nginx or a third-party operator with env-specific values per cluster.

**Example:** Bad image tag — `helm rollback my-release 1` restores prior revision quickly.

## Pros/Cons or Trade-offs

- **Pro:** Repeatable installs; rich ecosystem charts.
- **Con:** Templating complexity and surprise defaults if you do not read values.

## Comparison

- vs raw `kubectl apply`: Helm tracks revisions and packages.
- vs Kustomize: Helm packages params; Kustomize overlays plain manifests.

## Mistakes to Avoid

- `--set` sprawl unreviewed in CI.
- Upgrading without checking `helm get values` drift.
- Assuming chart `kind` quirks without reading CRD notes in the chart README.
