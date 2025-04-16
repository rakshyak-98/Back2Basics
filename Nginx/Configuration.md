> [!INFO] reverse proxy + static file server
> `nginx` is not an app server, it's reverse proxy + static file server. It cannot directly execute dynamic code (like NodeJS, Python, PHP)


> [!WARNING] nginx doesn't allow variables in alias.
- if you must use dynamic/templated configs: generate them via a build script or use templating engines (e.g., Ansible / Jinja, envsubst)

- use `nginx` to serve static files `/public`.
- Proxy all dynamic routes to NextJS `localhost:3000`


```sh
sudo truncate -s 0 /var/log/nginx/access.log; # clearn log
```

### Image support
```js
// [next.config.js]
images: {
  domains: ['res.cloudinary.com'],
  remotePatterns: [
    {
      protocol: "https",
      hostname: "**",
    },
  ],
}
```

## Folder
`fastcgi.conf` -> this is a standard Nginx config file used when Nginx acts as a reverse proxy for FastCGI servers.
```conf
location ~ \.php$ {
    include fastcgi.conf;
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
}

```

> [!INFO] Nginx itself does not execute dynamic code (like PHP, Python etc) instead, it forwards requests to external FastCGI servers and `fastcgi.conf` provides the necessary parameters for the communications.


