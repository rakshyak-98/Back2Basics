## Profiling and Monitoring
- have an build in profiler 
- monitoring tool: [Relic](https://newrelic.com/), [AppDynamics](https://www.appdynamics.com/), [pm2](https://pm2.io/) application performance in real-time.
## Efficient code practices
- Avoid blocking the event loop
- Use clustering: Utilize the node.js cluster module to take advantage of multi-core systems by creating child process.
- optimizing data base queries.
## Caching
- In-memory caching: Use in-memory caching solutions [Redis]() or [Memcached]() to store frequently accessed data.
- HTTP caching: Implement HTTP caching headers to reduce the load on server.
## Load Balancing
- User load balancer like [Nginx]() or [HAProxy]() to distribute incoming traffic across multiple servers.
## Compression
- Gzip compression: Enable gzip compression to reduce the size of the response body and improve load time.