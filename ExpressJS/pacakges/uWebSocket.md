[[pacakges]]

# uWebSocket

> One-line: what / why for **uWebSocket** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

used for real-time applications that require efficient networking, such as chat applications, trading platforms, multiplayer games.
- fast due to its efficient event loop and memory management.
- popular alternative to frameworks like [[Socket IO]]
- support secure WebSocket connections (`wss://`) with SSL/TLS
```shell
npm install uWebSockets.js
```
```js
const uWS = require('uWebSockets.js');
uWS.App().ws('/*', {
  open: (ws) => {
    console.log('A client connected!');
  },
  message: (ws, message, isBinary) => {
    ws.send(message, isBinary);
  },
  close: (ws, code, message) => {
    console.log('A client disconnected');
  }
}).listen(9001, (token) => {
  if (token) {
    console.log('Listening on port 9001');
  }
});
```

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
