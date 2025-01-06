A reverse proxy is used by the server-side to accept request from clients on behalf of the actual server, hiding the server's identity. The response from the back-end server is sent back to the client through the reverse proxy.

A reverse proxy is used by the server to handle incoming traffic from multiple clients and distribute it to the back-end servers.
- it is typically used to protect the actual server's infrastructure and load balance traffic.

> [!INFO] Reverse proxies can keep a [cache](https://en.wikipedia.org/wiki/Cache_(computing)) of static content, which further reduces the load on these internal servers and the internal network.