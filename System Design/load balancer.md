load balancer is a component that distributes incoming traffic across multiple servers so that no single server becomes overloaded.

## Algorithms

**Static**
[[load balancer/Static/Round Robin]] sequence distribution in rotating, basic level of even distribution.
[[load balancer/Static/Weighted Round Robin]] assign different wait (capability) to server.
[[load balancer/Static/IP Hash]] unique hash value of the ip client, maintaining sticky session, shopping data, same server to have the user consistent user data.

**Dynamic**
[[load balancer/Dynamic/Least connections]] direct to the server currently to the server having few  active connection, usefully server different processing speed, different request processing speed, taking long time. go to least amount of activity.
[[load balancer/Dynamic/Least Response Time]] track the current state with also the average time server took to response.
[[load balancer/Dynamic/Least bandwidth routing]] balance the throughput between the server consuming least amount of data (measured in MBs bandwidth), large data transfers - video streaming, file streaming. 
[[load balancer/Dynamic/Resource based]] running agent in backend service of gather the server usage and stats and report back to the load balancer, need more monitoring system.
[[Random]]

- high traffic, suddenly increase of massive traffic. act as buffer distributing the incoming request to the multiple servers. improve the up time, and resilience of the application.
- load-balancer significantly increase the application response. user experience faster loading time.
- fault tolerance, resilient system (availability, scalability)

choosing the load balancer algo - unique characteristic of the application
decision metric - capacity of the server, all heterogeneous, nature of the request application handles, general resource demand, or request need more computing power.

## Load Balancers

[[Nginx]]
[[AWS ELB]]
[[Kubernetes/Ingress Gateway]]

## Related

[[ALB (Application Load Balancer)]] · [[connection chrun]] · [[AWS Networking]] · [[AWS]]
