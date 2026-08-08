[[Kubernates]]

# You are essentially reading from or writing to etcd through the kubernetes API server.

> You are essentially reading from or writing to etcd through the kubernetes API server. — etcd — highly reliable, distributed key-value store that serves as the central data

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

etcd -> highly reliable, distributed key-value store that serves as the central data store and brain of Kubernetes.
- highly-available key-value database designed specifically for distributed systems. It stores all critical configuration data, metadata, and the current state of the Kubernetes cluster.
> [!INFO]
> Kubernetes uses etcd as its _primary backing store_. Everything in Kubernetes is stored in etcd, including
> - cluster state, Service discovery information, Cluster configuration, Resource metadata and status, API objects.
```bash
kubectl get pods
kubectl apply -f deployment.yaml
```

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
