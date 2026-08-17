[[kubectl]] [[INDEX]]

# Kubernates CLI

> kubectl — cluster context, workloads, and debugging.

---

## kubectl

### Scaling chain

From [[kubectl]].

```bash
kubectl get deploy,hpa,pdb -n prod -l app=api
kubectl describe hpa -n prod api
kubectl get events -n prod --field-selector reason=FailedScheduling | tail -10
kubectl top nodes
```
