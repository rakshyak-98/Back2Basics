[[helm]]

# helm

> helm — the kind field is not part of the basic required fields, but it can be added to specify the type of chart. The kind field should

---

## How it works

```bash
helm list
helm get values
```
- The `kind` field is not part of the basic required fields, but it can be added to specify the type of chart. The `kind` field should be used for custom resources, as it helps Helm understand how to process the resource during installation and upgrade


## Configuration and commands

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-release bitnami/nginx
helm upgrade my-release bitnami/nginx -f values.yaml
helm rollback my-release 1
```

---


## Where to go next

| Symptom / need | Go to |
|----------------|-------|
| … | [[…]] |


## Related topics in this domain

- …: [[…]]


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Pending install forever | CRD missing; webhook timeout | `kubectl get events`; install CRDs first |
| Wrong chart version | repo not updated | `helm repo update`; pin version in install |
| Values ignored | wrong file; subchart key | `helm get values`; nest under chart name for subcharts |
| Release exists cannot install | name collision | `helm uninstall` or choose new release name |

---


## Gotchas

> [!WARNING]
> Helm stores release state in cluster **Secrets** — protect etcd backups.

---


## When not to use

- Do not hand-edit rendered manifests in the cluster — change values and upgrade.


---


## Related

[[helm]]

## Sources

- [Wikipedia — helm](https://en.wikipedia.org/wiki/helm)
