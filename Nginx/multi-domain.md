

Add fake domains to `/etc/hosts`
```
127.0.0.1   api.localhost
127.0.0.1   shop.localhost
127.0.0.1   blog.localhost
```
- You can `ping api.localhost` and it'll look back to your machine.

Create local folders
```bash
sudo mkdir -p /var/www/api /var/www/shop /var/www/blog;
```

Configure Nginx
- create separate server blocks `/etc/nginx-sites-available/multidoman`;

```nginx
server {
    listen 80;
    server_name api.localhost;

    root /var/www/api;
    index index.html;
}

server {
    listen 80;
    server_name shop.localhost;

    root /var/www/shop;
    index index.html;
}

server {
    listen 80;
    server_name blog.localhost;

    root /var/www/blog;
    index index.html;
}
```

- enable it
```bash
sudo ln -s /etc/nginx/site-available/multidomain /etc/nginx/sites-enable;
sudo nginx -t; # test config.
sudo systemctl reload nginx;
```


### TLS self-signed certificate

Generate a self signed certificate [[openssl#Generate self signed certificate]]
- permissions: `nginx` must read the `.crt` and `.key`.
- port 443 may be in use -> stop other services if needed.

```nginx
server {
	listen 443 ssl;
	server_name shop.localhost;
	
	ssl_certificate /etc/nginx/certs/shop.localhost.crt;
	ssl_certificate_key /etc/nginx/certs/shop.localhost.key;
	
	root /var/www/shop;
	index index.html;
}

# Optional: redirects HTTP -> HTTPS
server {
	listen 80;
	server_name shop.localhost;
	return 301 https://$host$request_uri;
}
```

### Reverse proxy

Run a Local API [[expressjs]]

> [!NOTE]
> Trailing slash in `proxy_pass` matters

Configure Nginx for Reverse Proxy
Edit your `/etc/nginx/sites-available/multidomain` and update the `api.localhost` block
```nginx
server {
	listen 80;
	server_name api.localhost;
	location / {
		proxy_pass http://127.0.0.1:3000;
		
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forward-For $proxy_add_x_forward_for;
		proxy_set_header X-Forward-Proto $scheme;
	}
}
```
```nginx
location /users/ {
	proxy_pass http://127.0.0.1:3000/;
}

location /auth/ {
	proxy_pass http://127.0.0.1:4000/;
}
```
-> `/users/*` goes to one backend, `/auth/*` goes to another.

Load balancing multiple APIs

```nginx
upstream api_backend {
	server 127.0.0.1:3000;
	server 127.0.0.1:3001;
}
server {
	listen 80;
	server_name api.localhost;
	
	location / {
		proxy_pass http://api_backend;
	}
}
```