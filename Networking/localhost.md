
## What localhost means to each devices
`localhost` always means the device running the app, not "my dev machine" or "where the API lives".

| Where the app runs            | What `http://localhost:3000` points to                        |
| ----------------------------- | ------------------------------------------------------------- |
| Your computer (Linux desktop) | Your computer — same machine as the backend                   |
| Android emulator              | The emulator (special case: use `10.0.2.2` to reach the host) |
| Physical phone/tablet<br>     | The phone itself — not your computer                          |

- On a physical device, that URL tries to open port 3000 on the phone. Nothing is listening there, so the request fails and you get “Unable to connect to the server…”

## Why you need your computer’s IP

The backend runs on your development machine (`npm run dev` in `backend/`). The phone is a separate device on the same Wi‑Fi/LAN.

To reach your computer, the phone must use its network address, for example:

`http://192.168.1.50:3000/api`

That tells the phone: “send this request to the machine at 192.168.1.50 on port 3000,” which is your laptop/desktop.

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