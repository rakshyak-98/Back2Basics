boot up sequence

```
kubctl apply;
```
- pods start pull the image app run
- asynchronous control loop 

- kubctl api server
- replica set controler
- pod objects
- kubctl scheduler, for unbound pods, filtering and scoring algo, pod binding
- continer run time, network namespace
- inti container: setup task and successfully die, cannot run in parellel, design to be blocking
- schema migration, before db container boots up
- migratino tool require root sudo access, how to avoid remote comamnd exection attack
- kub prob, startup, liveness, readyness
- liveness : never put external dependency in liveness prob, only localize application health, return 500 status code and stay alive
- kube 1.29, restart policy
- creadentail managmenet 
	- no hardcoded password on yaml
	- valut agent get into the pod, no manual sit card update
	- pod spec to api server, api server pauses the deployment
	- 