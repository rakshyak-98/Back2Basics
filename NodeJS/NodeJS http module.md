### Use case for `http.createServer(app)`
- this approach is useful in scenarios where you need more control over the HTTP server beyond what `app.linsten(port)` provides in Express.

##### Enabling WebSockets
- `http.createServer(app)` allows integrating WebSockets for real-time communication.
```js
import express from 'express';
import http from 'http';
import { Server } from 'socket.io';

const app = express();
const server = http.createServer(app);
const io = new Server(server); // Attach WebSockets to the HTTP server

io.on('connection', (socket) => {
    console.log('A user connected');
    socket.on('message', (msg) => io.emit('message', msg)); // Broadcast messages
});

server.listen(3000, () => console.log('Server running on port 3000'));

```

##### Handling Both HTTP & HTTPS Requests
```js
import express from 'express';
import http from 'http';
import https from 'https';
import fs from 'fs';

const app = express();
const httpServer = http.createServer(app);
const httpsServer = https.createServer(
    { key: fs.readFileSync('key.pem'), cert: fs.readFileSync('cert.pem') },
    app
);

httpServer.listen(80, () => console.log('HTTP Server running on port 80'));
httpsServer.listen(443, () => console.log('HTTPS Server running on port 443'));

```

##### Graceful shutdown
- when shutting down a server (e.g., during deployments or errors), you may need to properly close connections before exiting
```js
import express from 'express';
import http from 'http';

const app = express();
const server = http.createServer(app);

server.listen(3000, () => console.log('Server started on port 3000'));

process.on('SIGTERM', () => {
    console.log('Shutting down gracefully...');
    server.close(() => {
        console.log('All connections closed. Exiting.');
        process.exit(0);
    });
});

```