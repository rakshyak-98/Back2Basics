[[Kubernates]]

# You are essentially reading from or writing to etcd through the kubernetes API server.

> You are essentially reading from or writing to etcd through the kubernetes API server. — etcd — highly reliable, distributed key-value store that serves as…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** You are essentially reading from or writing to etcd through the kubernetes API server. — etcd — highly reliable, distributed key-value store that serves as…

etcd -> highly reliable, distributed key-value store that serves as the central data store and brain of Kubernetes.
- highly-available key-value database designed specifically for distributed systems. It stores all critical configuration data, metadata, and the current state of the Kubernetes cluster.

## Standard config / commands

```bash
kubectl config view
kubectl config use-context prod
kubectl config set-context --current --namespace=team-a
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| wrong cluster targeted | current context | `kubectl config current-context`; switch context |
| certificate expired | client cert on kubeconfig | Refresh credentials; `kubeadm` or cloud IAM |
| namespace not found | typo; context default namespace | `kubectl get ns`; set `-n` explicitly |

---

## Gotchas

> [!WARNING]
> `~/.kube/config` merges multiple clusters — **context** picks cluster + user + default namespace.

---

## When NOT to use

- Do not commit kubeconfig with embedded credentials to git.


---

## Related

[[Kubernates]]
