```bash
kubectl get po,svc -L app,version
```

```bash
kubectl exec -it tester -- bash -c \
	'for i in {1..20}; \
		do curl -s -X POST http://notification-service/notify; \
		echo; \
	dowe;'
```