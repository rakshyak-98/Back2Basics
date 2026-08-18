[[helm]]

# cli

> cli — helm repo add <namespace> <url> <flag>;

## Mental model

**Say it in one breath:** cli — helm repository add <namespace> <url> <flag>;

```bash
helm repo add <namespace> <url> <flag>;
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
help repo udpate;
help search repo nginx;
help search repo ingress;
```
```bash
helm install my-ingress ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.service.type=NodePort
```
```bash
helm list -A;
helm status my-ingress -n ingress-nginx;
helm upgrade my-ingress ingress-nginx/ingress-nginx -n ingress-nginx;
helm uninstall my-ingress -n ingress-nginx;
```

## Standard config / commands

```bash
helm list -A
helm status my-release -n prod
helm get manifest my-release
helm template my-release ./chart --debug
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| cannot re-use a name that is still in use | failed release not purged | `helm uninstall`; or `helm history` + rollback |
| connection refused to Kubernetes | kubeconfig context | `kubectl cluster-info`; fix `KUBECONFIG` |
| chart not found | repo not added | `helm search repo` after `helm repo add` |

## Gotchas

> [!WARNING]
> `helm template` renders locally — it does not prove the cluster will accept resources.

## When NOT to use

- Do not use `helm install` in production without version-pinned charts in CI.

## Related

[[helm]]
