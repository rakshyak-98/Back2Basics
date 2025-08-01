```sh
sudo nginx -t;
sudo nginx -t -c <full path to custom nginx.conf>;
sudo nginx -c <full path to custom nginx confi file>; # run with custom config
sudo nginx -s reload;
```
- use `-c` if you're running a config that's not in the default location.

```sh
sudo nginx -c <full path to nginx confi file> -g "daemon off"; # run in foreground
```

> [!INFO] reverse proxy + static file server
> `nginx` is not an app server, it's reverse proxy + static file server. It cannot directly execute dynamic code (like NodeJS, Python, PHP)

```conf
http {
  server{
    listen 8080;
    server_name localhost;
    location /_next/status/ {
      alias /home/rakshyak/GitHub/Booking-engine/gotrip/.next/static/;
      access_log off;
    }

    location /public/ {
      alias /home/rakshyak/GitHub/Booking-engine/gotrip/public/img/;
    }

    location / {
      proxy_pass http://127.0.0.1:3000;
    }
  }
}

events {}

```


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

## site-enable and site-available
`/etc/nginx/sites-enabled` -> stored active in live Nginx usually contains `symlinks` to files in `site-available`

- easy to enable/disable site
```shell
sudo unlink /etc/nginx/sites-enabled/myapp;
```

> [!INFO] put files inside `/etc/nginx/site-available` create symbolic link to the `/etc/nginx/site-enable`
- `next.conf.ts` -> add `base_path` and `leadingslash: true` property in `nextConfig`
- `basePath` must not have trailing `/`