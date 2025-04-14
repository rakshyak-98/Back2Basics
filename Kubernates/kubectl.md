```sh
kubectl log --since=5m <pod name>;
kubectl log -f <pod name>;
kubectl logs -l app=<pod label> -f; # collect logs from all posd with --selector
```

```sh
kubectl get pods -l app=<pod label> -o name; # find all pods name.
kubectl logs -l app=my-app -n <namespace>;
```