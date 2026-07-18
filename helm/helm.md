```bash
helm list
helm get values 

```

- The `kind` field is not part of the basic required fields, but it can be added to specify the type of chart. The `kind` field should be used for custom resources, as it helps Helm understand how to process the resource during installation and upgrade

## Deployment

Helm is package manager for kubernetes.
- tool to install, upgrade, and manage complex applications on Kubernetes (like the Nginx Ingress Controller). Instead of manually applying many YAML files, Helm uses a pre-packaged bundle called a Chart.

Chart -> contains all the necessary Deployment, Services, ConfigMaps, RBAC roles, etc. in one place.

### Deploy controller

installing and running the actual software (application) that will implement and enforce your ingress rules.

> [!NOTE]
> You can create hundreds of Ingress YAML files, but nothing will work until you deploy the ingress controller.

### What happens when you deploy the controller

When you deploy the Nginx Ingress Controller, Kubernetes creates the following:
	- a deployment (one or more pods) running the NGINX web server.
	- A service (NodePort or LoadBalancer) to expose the controller.
	- RBAC permissions, ConfigMaps, and other supporting resources.
	- The controller starts watching all ingress resources in the cluster.

Once deployed, the controller automatically:
	- reads your YAML file.
	- Configure NGINX accordingly
	- Routes external traffic to your backend service (`/v1` `/v2` etc.).
