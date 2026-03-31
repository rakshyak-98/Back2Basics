```sh
kubectl log --since=5m <pod name>;
kubectl log -f <pod name>;
kubectl logs -l app=<pod label> -f; # collect logs from all posd with --selector
```

```sh
kubectl get pods -l app=<pod label> -o name; # find all pods name.
kubectl logs -l app=my-app -n <namespace>;
```

## Setup ingress

```bash
kubectl version --client;
```

```bash
kubectl get pods -A;
kubectl config view;
```

```bash
kubectl config get-contexts;
```

### Deployment

```bash
kubectl create deployment <deployment name> --image=<image tag>;
kubectl scale deployment/my-first-deployment --replicas=3;
kubectl scale deployment/my-first-deployment --replicas=2; # scale down
kubectl set image deployment my-first-deployment nginx=httpd:alpine;
```

```bash
kubectl get deployment my-first-deployment;
kubectl get pods -l app=my-first-app;
kubectl describe deployment my-first-deployment;
```

```bash
kubectl apply -f <filename>; # apply a configuration change to a resource from a file or stdin.
```