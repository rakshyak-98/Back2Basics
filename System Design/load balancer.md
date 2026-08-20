load balancer is system or device, collection of backend servers, primary distribute application traffic across these servers, prevent any single server from completely overwhelmed. Intelligently deliver the incoming request to capable server.
- high traffic, suddenly increase of massive traffic. act as buffer distributing the incoming request to the multiple servers. improve the up time, and resilience of the application.
- load-balancer significantly increase the application response. user experience faster loading time.
- fault tolerance, resilient system (availability, scalability)

**Set of rules to**
two main category
static - pre determined rules, they don't consider current workload in that exact movement
	- round robin -> sequence distribution in rotating, basic level of even distribution.
	- waited round robin -> assign different wait (capability) to server.
	- IP hash -> unique hash value of the ip client, maintaining sticky session, shopping data, same server to have the user consistent user data.

dynamic - examine current state of server.
	-	least connections -> direct to the server currently to the server having few  active connection, usefully server different processing speed, different request processing speed, taking long time. go to least amount of activity.
	-	least response timing -> track the current state with also the average time server took to response.
	-	least bandwidth routing -> balance the throughput between the server consuming least amount of data (measured in MBs bandwidth), large data transfers - video streaming, file streaming. 
	-	
	-	resource based - running agent in backend service of gather the server usage and stats and report back to the load balancer, need more monitoring system.

choosing the load balancer algo - unique characteristic of the application
decision metric - capacity of the server, all heterogeneous, nature of the request application handles, general resource demand, or request need more computing power.