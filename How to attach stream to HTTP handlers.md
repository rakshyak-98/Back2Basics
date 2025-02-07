## Streaming file download
```js
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();

app.get('/download', (req, res) => {
  const filePath = path.join(__dirname, 'large-file.txt');
  const readStream = fs.createReadStream(filePath);

  res.setHeader('Content-Disposition', 'attachment; filename="large-file.txt"');
  res.setHeader('Content-Type', 'text/plain');

  readStream.pipe(res); // Stream file data to response
});

app.listen(3000, () => console.log('Server running on port 3000'));

```
- `fs.createReadStream()` read file chunks efficiently
- `.pipe(res)` sends data directly to the client, reducing memory usage.

## Streaming file upload
```js
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();

app.get('/download', (req, res) => {
  const filePath = path.join(__dirname, 'large-file.txt');
  const readStream = fs.createReadStream(filePath);

  res.setHeader('Content-Disposition', 'attachment; filename="large-file.txt"');
  res.setHeader('Content-Type', 'text/plain');

  readStream.pipe(res); // Stream file data to response
});

app.listen(3000, () => console.log('Server running on port 3000'));

```

> [!NOTE] When streaming data in NodeJs (including Express), you must explicitly handle stream events `end`, `error`.
- without this the request might close before the upload finishes.
- the client might receive an incomplete response or no confirmation


### Proxying data (Streaming Request and Response)
```js
const express = require('express');
const { request } = require('https');

const app = express();

app.use('/proxy', (req, res) => {
  const proxyReq = request('https://example.com', { method: req.method });

  req.pipe(proxyReq); // Forward request data  
  proxyReq.pipe(res); // Stream response back  
});

app.listen(3000, () => console.log('Proxy server running on port 3000'));

```
- `req.pipe(proxyReq)` forwards data to an external server.
- `proxyReq.pipe(res)` stream the response back to the client.