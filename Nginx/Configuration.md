
| Directive | Config                                          | Request           | Resolved Path                    |
| --------- | ----------------------------------------------- | ----------------- | -------------------------------- |
| root      | `location /images/ { root /var/www/static; }`   | `/images/cat.png` | `/var/www/static/images/cat.png` |
| alias     | `location /images/ { alias /var/www/static/; }` | `/images/cat.png` | `/var/www/static/cat.png`        |

[variables](https://nginx.org/en/docs/http/ngx_http_core_module.html#var_host)
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

### Run php project
To run a PHP project using Nginx, you need to configure it to pass `.php` files to `PHP-fpm`.

Edit or create config -> `/etc/nginx/sites-available/yourproject`

> [!NOTE]
> Even if Nginx runs as nginx, PHP-FPM (handling PHP execution) typically runs as www-data. Thus, www-data needs ownership or sufficient permissions (e.g., 755 for directories, 644 for files) to access your project files.

> [!NOTE]
> You change the owner to www-data (or ensure www-data has access) to allow PHP-FPM to:
> - Read PHP files for execution.
> - Write to directories (e.g., for uploads, logs, or framework caches like Laravel’s storage directory).
> - Avoid permission errors when PHP-FPM tries to access files owned by another user.

```nginx
server {
    listen 80;
    server_name localhost;

    root /var/www/html/yourproject;
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php7.4-fpm.sock; # adjust for your PHP version
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }
}

```

```bash
sudo ln -s /etc/nginx/sites-available/yourproject /etc/nginx/sites-enabled/

sudo systemctl restart php7.4-fpm;
sudo systemctl restart nginx;
```

## Configure nginx to handle different directory

```nginx
server {
    listen 80;
    server_name example.com;

    # Global root for static files (CSS, JS, images)
    root /var/www/global;

    index index.html index.htm;

    # Serve static assets directly from global root
    location / {
        try_files $uri $uri/ =404;
    }

    # PHP location with its own root
    location ~ \.php$ {
        root /var/www/phpapp;
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $request_filename;
        include fastcgi_params;
    }

    # Python (WSGI via uWSGI HTTP)
    location /py/ {
        root /var/www/pythonapp;
        proxy_pass http://127.0.0.1:8000;  # Gunicorn/uwsgi server
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Node.js app
    location /node/ {
        root /var/www/nodeapp; # Optional, for static files inside /node/
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
    }

    # Optional error logging
    error_log /var/log/nginx/multi-lang-error.log;
    access_log /var/log/nginx/multi-lang-access.log;
}

```

