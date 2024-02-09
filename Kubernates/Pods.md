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
### Splitting into multiple pods to enable Individual scaling
- a pod is basic unit of scaling.
- Kubernetess can't horizontally scale individual containers, instead it scales whole pods.
- when you scale up the number of instances of the pod to, let's say, two, you end up with two frontend containers and two backend containers.
- If you need to scale a container individually, this is a clear indication that it need to be deployed in a separate pod.
### Understanding when to use multiple containers in a pod
- main reason to put multiple containers into a single pod is when the application consists of one main process and one or more complementary processes.
For example, the main container in a pod could be a web server that serves files from a certain file directory, while an additional container periodically downloads content from an external source and stores it in the web server's directory.
### Deciding when to use Multiple containers in a Pod
- do they need to be run together or can they run on different hosts?
- do they represent a single whole or are they independent components?
- must they be scaled together or individually?
# Creating pods from YAML or JSON descriptors
- created by posting a JSON or YAML manifest to the Kubernetes REST API endpoint.
- defining all your Kubernetes Objects from YAML files makes it possible to store them in a version control system, with all the benefits it brings.
# Reference
- [Kubernetes API reference documentation](https://kubernetes.io/docs/reference/)
