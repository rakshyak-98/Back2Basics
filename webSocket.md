WebSocket provide full-duplex, bidirectional communication between a client and a server over a single TCP connection.
- WebSocket allow real-time data exchange without repeatedly polling the server.

#### Basic WebSocket Flow
- client initiates handshake via `ws://` or `wss://`
- server upgrades connection to WebSocket protocol
- client and server exchange messages bidirectionally
- connection remains open until one side close it


#### Setting proxy for WebSocket
this depends on whether you're configuring it on the client-side, server-side, or network-level.

### Client side (Browser WebSocket API)

> [!INFO] Browsers do not support WebSocket proxies 
> - via standard proxy settings (like HTTP/ HTTPS proxies). Instead use a WebSocket tunneling proxy (SOCKS or HTTP CONNECT method).

```shell
chrome --proxy-server="socks5://127:0.0.1:1000";

```
- this forces WebSocket connections through the SOCKS proxy.

#### Neginx as a WebSocket proxy

```nginx
location /ws/ {
	proxy_pass http://backend_server;
	proxy_set_header Upgrade $http_upgrade;
	proxy_set_header Connection 'Upgrade';
}

```