Ingress -> the rule you write
Ingress Controller -> The actual program that applies those rules
Deploy Controller -> Installing and starting that program

[Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- API object that manages external access to services within a kubernetes cluster, usually HTTP.
- provides a way to route traffic to different services based on the URL path, host or other criteria.

> [!INFO]
> Network administrators and security teams closely monitor and control ingress traffic using firewalls, ACLs and instrusion Detection Systems to prevent unauthorized access.

In Kubernetes, Ingress is a specific API resource that provides a standardized way to manage external HTTP and HTTPS access to services running inside the cluster.
- act as a smart routing layer at the edge of the cluster.
- it handles features such as URL-based routing, host-based routing, SSL/TLS termination, load balancing, and name-based virtual hosting.
- Ingress is implemented by an Ingress Controller (e.g., NGINX Ingress Controller, Traefik, HAProxy, or cloud-specific controllers like AWS ALB Ingress Controller).
- Unlike LoadBalancer or NodePort services, Ingress offers a more flexible, feature-rich, and cost-effective method for exposing multiple services through a single external IP or domain.