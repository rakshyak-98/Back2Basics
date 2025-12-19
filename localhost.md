
## How to host localhost with HTTPS

```bash
sudo apt install mkcert;
```

```bash
mkcert -install; # create and install Local CA (one-time)
```

```text
The local CA is now installed in the system trust store! ⚡️
Warning: "certutil" is not available, so the CA can't be automatically installed in Firefox and/or Chrome/Chromium! ⚠️
Install "certutil" with "apt install libnss3-tools" and re-run "mkcert -install" 👈

```

**Install additional package**

```bash
apt install libnss3-tools
```

```text
The local CA is already installed in the system trust store! 👍
The local CA is now installed in the Firefox and/or Chrome/Chromium trust store (requires browser restart)! 🦊

```

### Express config

```bash
mkdir cert; # at working root directory of express application.
mv cert;
mkcert localhost 127.0.0.1 ::1

```

```text
Created a new certificate valid for the following names 📜
 - "localhost"
 - "127.0.0.1"
 - "::1"

The certificate is at "./localhost+2.pem" and the key at "./localhost+2-key.pem" ✅

It will expire on 18 March 2028 🗓

```

```js
import express from 'express';
import https from 'https';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();

// ... your app setup

const options = {
  key: fs.readFileSync(path.join(__dirname, 'localhost+2-key.pem')),
  cert: fs.readFileSync(path.join(__dirname, 'localhost+2.pem'))
};

https.createServer(options, app).listen(3000, () => {
  console.log('Express HTTPS server running at https://localhost:3000');
});
```

## Frontend Nginx config

**vite config**

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'

export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key: fs.readFileSync('localhost+2-key.pem'),
      cert: fs.readFileSync('localhost+2.pem'),
    },
    port: 3000,
  },
})
```