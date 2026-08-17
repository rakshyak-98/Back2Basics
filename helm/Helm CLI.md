[[Helm CLI]] [[INDEX]]

# helm CLI

> Helm CLI — repos, install, upgrade, rollback.

---

## Helm CLI

From [[Helm CLI]].

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
