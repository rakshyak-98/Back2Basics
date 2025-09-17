

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