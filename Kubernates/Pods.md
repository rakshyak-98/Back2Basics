- it’s common for pods to contain only a single container.
- pod does contain multiple containers, all of them are always run on a single worker node. It never spans multiple worker nodes.

### Why we need pods

Understanding why multiple containers are better than one container running multiple processes.

- you should not run multiple processes in a single container.
- container are designed to run only a single process per container (unless the process itself spawns child process).

> [!Note] If you run multiple unrelated process in a single container, it is your responsibility to keep all those process running, manage their logs.

- container with multiple processes include a mechanism for automatically restarting individual processes if they crash.
- all those process will log to same standard output, so you’d have hard time figuring out what process logged what.

### Understanding pods

You’re not supposed to group multiple processes into a single container, it’s obvious you need another higher-level construct that will allow you to bind containers together and manage them as a single unit. This is the reasoning bind containers.

- manage all the container as a single unit.
- a pod container allows you to run closely related processes together and provide them with the almost same environment as if they were all running in a single container, while keeping them somewhat isolated.
### Understanding the partial isolation between container of the same Pod
- want to isolate group of containers.
- want each container inside group to share certain resources, although not all, so that're not fully isolated.
>[!Note] all containers of a pod share the same set of Linux namespace instead of each container having its own set.

All container of a pod run under the same Network and [[UTS namespace]] , they all share the same hostname and network interface, [[IPC namespace]].
- can also share the same PID namespace, but that feature isn't enable by default.
>[!Note] When containers of the same pod use separate PID namespaces, you only see the container's own process when running `ps aux` in the container.

- Most of the file system come from the container image, by default, the filesystem of each container is fully isolated from other containers.
- However it's possible to have them share file directories using a Kubernetes concept a *Volume*.
### How container share the same IP and Port space
This means processes running in containers of the same pod need to take care not to bind to the same port numbers or they'll run into port conflicts.
- each pod has a separate port space, so container is different pod do not run in port conflict.
- all the container in a pod also have the same loopback network interface, so a container can communicate with other containers in the same pod through localhost.
#### Introducing the flat Inter-pod network
- all pod in Kubernetes cluster reside in a single flat, shared, network-address space, which means every pod can access every other pod at the other pod's IP address.
- No NAT gateway exist between them.
- When two pods send network packets between each other, they'll each see the actual IP address of the other as the source IP in the packet.
- each pod gets a [[routable IP address]] and all other pods see the pod under that IP address.
- it doesn't matter if two pods are scheduled onto a single or onto different worker nodes. in both cases the containers inside those pods can communicate with each other across the flat NAT-less network, much like LAN, regardless of the actual inter-node network topology.
- this is achieved through an additional software-defined network layered on top of the actual network.