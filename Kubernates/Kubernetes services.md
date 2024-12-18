in Kubernetes, a service is a method for exposing a network application that is running as one or more [[Pods]] in your cluster.

A Service is an abstraction that defines a logical set of [[Pods]] and a policy to access them.
- It enables seamless communication between different parts of an application and external clients by providing a stable endpoint, even as the underlying Pods may change.
- Service decouple the frontend from backend Pods, ensuring consistent access despite Pod restarts or scaling operations

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
   app.kubernetes.io/name: MyApp
  ports:
   - port: 80
  # By default and for convenience, the `targetPort` is set to
  # the same value as the `port` field.
   targetPort: 80
   # Optional field
   # By default and for convenience, the Kubernetes control plane
   # will allocate a port from a range (default: 30000-32767)
   nodePort: 30007
```