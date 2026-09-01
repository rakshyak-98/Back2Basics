A reverse proxy is used by the server-side to accept request from clients on behalf of the actual server.

- handle incoming traffic from multiple clients and distribute it to the **application servers**.

> [!INFO] Reverse proxies can keep a [cache](https://en.wikipedia.org/wiki/Cache_(computing)) of static content.


**Load balancing multiple server**
```nginx
http {
    upstream backend {
        server 127.0.0.1:3001;
        server 127.0.0.1:3002;
        server 127.0.0.1:3003;
    }

    server {
        listen 80;
        server_name api.example.com;

        location / {
            proxy_pass http://backend; # nginx internal use to route to upstream group

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```