is a communication protocol that uses JSON-RPC as the format for sending requests and responses between two points

> One program asks another program to run a function, using JSON messages.

From client
```json
{
  "jsonrpc": "2.0",
  "method": "getUser",
  "params": {
    "id": 123
  },
  "id": 1
}
```

Server send response
```json
{
  "jsonrpc": "2.0",
  "result": {
    "name": "Alice",
    "email": "alice@example.com"
  },
  "id": 1
}
```
- Client calling the `getUser()` function on another computer

**JSON-RPC defines a standardized JSON structure for things like:**
- method — the operation to perform
- params — arguments to that operation
- id — identifies the request
- result — successful response
- error — failed response