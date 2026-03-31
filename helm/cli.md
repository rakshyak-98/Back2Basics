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