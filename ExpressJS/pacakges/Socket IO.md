# Why it is http:// Instead of ws:// in the Web Socket server setup?

> [!INFO] A pure WebSocket server can only handle WebSocket connections. Using an HTTP server allows us to support both WebSocket and REST API endpoints in a single applicatoin.

if we start a raw WebSocket server `ws://`, we lose the ability to use Express middleware (CORS, authentication, etc.)

> [!INFO] Many reverse proxies (NGINX, AWS, ALB, Cloudflare) expect WebSocket to start as HTTP.

> [!INFO] If you use WebSockets over HTTP polling (long polling via HTTP requests) instead of `ws://`, Express middleware will apply because every request is an HTTP request.
- However, native WebSocket `ws://` do not trigger express middleware, so you must handle authentication separately.