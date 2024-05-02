- make use of the state where one direction is closed and the other is still open in TCP connection.
- unidirectional use of TCP is called TCP half-open.
	- A cannot send any more data, but can still receive from B.
	- B gets EOF, but can still send to A.
>[!NOTE] Node.js do not support half-open by default, and are automatically closed when other side sends or receives EOF.
```javascript
let server = net.createServer({allowHalfOpen: true});
// server.end() will no longer close the connection, use sockett.destroy()
```
