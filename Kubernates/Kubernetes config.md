etcd -> highly reliable, distributed key-value store that serves as the central data store and brain of Kubernetes.
- highly-available key-value database designed specifically for distributed systems. It stores all critical configuration data, metadata, and the current state of the Kubernetes cluster.

> [!INFO]
> Kubernetes uses etcd as its _primary backing store_. Everything in Kubernetes is stored in etcd, including
> - cluster state, Service discovery information, Cluster configuration, Resource metadata and status, API objects.

```bash
# You are essentially reading from or writing to etcd through the kubernetes API server.
kubectl get pods
kubectl apply -f deployment.yaml
```