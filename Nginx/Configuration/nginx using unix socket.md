
```bash
sudo mkdir -p /var/run/my-api;
sudo chown www-data:www-data /var/run/my-api
```

> Make sure Express app listen on the Unix socket

```js
// server.js (or index.js)
import express from 'express';
const app = express();

// ... your routes, middleware, etc.

const SOCKET_PATH = '/var/run/my-api/app.sock';

// Remove any old socket file first (important!)
import fs from 'fs';
if (fs.existsSync(SOCKET_PATH)) {
  fs.unlinkSync(SOCKET_PATH);
}

app.listen(SOCKET_PATH, () => {
  console.log(`API running on Unix socket: ${SOCKET_PATH}`);
  
  // Fix permissions so Nginx can connect
  fs.chmodSync(SOCKET_PATH, '775');   // or 777 if still having issues
});
```

> Run app with the correct user (important)
> nginx usually runs as `www-data` or `nginx`. So start your Node.js process as the same user

```bash
pm2 start dist/server.js --name my-api --user www-data;
```

> `/etc/systemd/system/my-api.service`

```ini
[Unit]
Description=My Node.js API
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/home/youruser/my-api
ExecStart=/usr/bin/node dist/server.js
Restart=always
Environment=NODE_ENV=production

# Clean up old socket on restart
ExecStartPre=/bin/rm -f /var/run/my-api/app.sock

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now my-api
```

> Nginx config for unix socket

```nginx
server {
    listen 80;
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    # SSL config here if using HTTPS...

    location / {
        proxy_pass http://unix:/var/run/my-api/app.sock;
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # These are required for WebSockets (if you ever use them)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Optional: health check endpoint
    location /health {
        proxy_pass http://unix:/var/run/my-api/app.sock;
    }
}
```

```bsh
sudo nginx -t && sudo systemctl reload nginx
```

> Verify it works

```bash
ls -la /var/run/my-api/app.sock; # socket exists and has correct permissions

curl --unix-socket /var/run/my-api/app.sock http://localhost
```

### Performance difference

|Method|Requests/sec|Latency (avg)|
|---|---|---|
|TCP localhost:3000|~18,500|2.1 ms|
|Unix socket|~24,000+|1.4 ms|