## Why it is http:// Instead of ws:// in the Web Socket server setup?

- WebSocket start as an HTTP request and then upgrade to the WebSocket protocol.
- The client sends an HTTP request and then upgrade to the WebSocket protocol.
- The client sends an HTTP handshake request `Upgrade: websocket` header.
- The server responds with `101` Switching Protocols, establishing a WebSocket connection.

> [!INFO] A pure WebSocket server can only handle WebSocket connections. Using an HTTP server allows us to support both WebSocket and REST API endpoints in a single applicatoin.

> [!INFO] Using http as the base server ensures that express (which handles routes, authentication, and middleware) can still manage requests before the WebSocket upgrade happens.

if we start a raw WebSocket server `ws://`, we lose the ability to use Express middleware (CORS, authentication, etc.)

> [!INFO] Many reverse proxies (NGINX, AWS, ALB, Cloudflare) expect WebSocket to start as HTTP.

> [!INFO] If you use WebSockets over HTTP polling (long polling via HTTP requests) instead of `ws://`, Express middleware will apply because every request is an HTTP request.
- However, native WebSocket `ws://` do not trigger express middleware, so you must handle authentication separately.