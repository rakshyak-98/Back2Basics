```javscript
app.set()
```
- may store any value that you want, but certain names can be used to configure the behavior of the server.
- [app settings table](https://expressjs.com/en/4x/api.html#app.settings.table)

>[!NOTE ] calling `app.set('foo', true)` for a boolean property is same as calling `app.engable('foo')`. Similarly `app.set('foo', false)` is `app.disable('foo')`

> [!INFO] empty object (`{}`) if there was no body to parse, the `Content-Type` was not matched, or an error occurred.

>[!INFO] `reviver` parameter in `JSON.parse` is a function that allows you to transform the values during the parsing process

```javascript
const jsonString = '{"name": "John", "age": 25, "birthdate": "1990-01-15T00:00:00Z"}';

// Reviver function to convert birthdate string into a Date object
const reviver = (key, value) => {
  if (key === 'birthdate') {
    return new Date(value);
  }
  return value;
};

const parsedObject = JSON.parse(jsonString, reviver);

console.log(parsedObject);
// Output: { name: 'John', age: 25, birthdate: 1990-01-15T00:00:00.000Z }

console.log(parsedObject.birthdate instanceof Date);  // true
```

### Inspecting
```js
console.log(app._router.stack);
```
- property holds middleware and route definitions.

### User case for `http.createServer(app)`
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