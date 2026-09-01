[[Reverse Proxy]] Between users and application server. Selects an upstream server per request.
- You can add, remove, replace, or move applications server without requiring clients to know where those servers are.

|Role|What Nginx does|
|---|---|
|Web server|Serves static files such as HTML, CSS, JS, images|
|Reverse proxy|Receives requests and forwards them to backend applications|
|Load balancer|Distributes requests across multiple application servers|
|TLS terminator|Handles HTTPS encryption/decryption at the edge|
|Cache|Stores responses to avoid repeatedly calling backend services|
|Traffic gateway|Applies rules such as routing, rate limiting and access control|

Nginx decides which internal server actually receives the request.
Control point **for of reverse proxy**:
- [[TLS termination]] handle HTTPS/TLS certification decryption.
- Authentication integration
- Request routing
- Rate limiting
- Logging
- Caching
- [[Load balancing]] it enables to **spread workload across multiple application instances.**
- Security policies