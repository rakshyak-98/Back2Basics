[[kubectl]] [[Pods]] [[kubectl pod creation]]

# Kubernetes config

> `kubectl` talks to the API server (backed by etcd) using a kubeconfig — contexts pick cluster, user, and default namespace so you read/write the right cluster brain.





## Interview Relevance
Interviewers ask how kubeconfig contexts work, that etcd holds desired state, and why embedding credentials in git is dangerous.

## Sources
- [Kubernetes — Organizing Cluster Access Using kubeconfig Files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) — deep-dive
- [Kubernetes — Operating etcd clusters for Kubernetes](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/) — overview

## Core Definition
Cluster state lives in etcd; you never edit etcd directly in normal ops — `kubectl` authenticates via kubeconfig and the API server mediates all reads/writes.

## Key Concepts
- **etcd:** highly available key-value store — control-plane brain for objects and desired state.
- **kubeconfig:** clusters + users + contexts; context = cluster + user + namespace.
- **Current context:** easy to hit the wrong cluster — always verify before apply/delete.
- **Credentials:** client certs, tokens, or cloud IAM exec plugins — rotate/expire.

## Technical Details
```bash
kubectl config view
kubectl config get-contexts
kubectl config current-context
kubectl config use-context prod
kubectl config set-context --current --namespace=team-a
```

Typical merge: multiple clusters in `~/.kube/config`; `use-context` switches the active trio.

| Symptom | Check | Fix |
|---------|-------|-----|
| wrong cluster targeted | current context | `kubectl config current-context`; switch context |
| certificate expired | client cert on kubeconfig | Refresh credentials; `kubeadm` or cloud IAM |
| namespace not found | typo; context default namespace | `kubectl get ns`; set `-n` explicitly |

## Real-World Applications
Laptop access to dev/stage/prod clusters, CI kubeconfigs via short-lived cloud IAM, and namespace defaults for team sandboxes.

**Example:** Before a production apply, `kubectl config current-context` shows `prod-east` and `-n payments` is set — avoiding a stage outage from the wrong context.

## Pros/Cons or Trade-offs
- **Pro:** One file can hold many clusters with clear context switching.
- **Con:** Merged configs make “wrong cluster” mistakes easy.
- **Con:** Long-lived embedded credentials in files are a leak risk.

## Comparison
- vs direct etcd access: always use the API server — etcd is for control-plane operators only.
- Day-to-day CLI → [[kubectl]]; object creation → [[kubectl pod creation]].

## Mistakes to Avoid
- Committing kubeconfig with embedded credentials to git.
- Applying manifests without checking `current-context`.
- Relying on the `default` namespace for production objects.
