Acts as a load balancer and [[Reverse Proxy]] for kubernetes cluster.
Nginx ingress is a ingress controller for Kubernetes that manages external access to services running in a kubernetes cluster. 
- enables secure and scalable HTTP(S) traffic routing to Kubernetes workloads. 
- rate limiting, IP whitelisting, and custom error page.

Load Balancing: Distributes traffic across multiple back-end pods to ensure reliability and scalability

SSL/TLS Termination: Handles HTTPS traffic by terminating SSL connections at the ingress layer.

Host-Based Routing: Routes requests based on URL paths or hostnames.

Authentication: Supports basic authentication, JWT, and OAuth2 integration.

### Example nginx ingress config file

```yaml
apiVersion: networking.k8s.io/v1 # must be appropriate version 
kind: Ingress # Always set to Ingress
metadata:
	name: basic-ingress # Name of the ingress resource
spec:
	rules: # specifies at leat one routing rule (host and path)
	- host: example.com
	http:
		paths:
		- path: /
		pathType: Prefix
		backend:
			service:
				name: my-service # Name of the target Kubernetes service
				port:
					number: 80 # Port number of the target service
```