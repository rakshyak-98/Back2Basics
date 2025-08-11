if you want nginx to handle other languages, you have two main routes.

> [!NOTE]
> - Each language needs its own backend -> nginx does not interpret code.
> - PHP works because of PHP-FPM (php FastCGI). For others, you need a similar FastCGI handler or an HTTP reverse proxy.

> [!INFO]
> You can run multiple handlers at once and let Nginx route based on file extensions or URL path.

## Use the language's own FastCGI handler
```nginx
location ~ \.py$ {
	fastcgi_pass unix:/run/uwsgi/python.sock;
	include fastcgi_params;
	fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

```bash
uwsgi --socket /run/uwsgi/python.sock --plugin python --wsgi-file app.py;
```

## Reverse proxy to an application server
- works for languages that run their own HTTP server (Node.js Django, Go etc).

```nginx
location /nodeapp/ {
	proxy_pass http://127.0.0.1:3000;
	proxy_set_header Host $host;
	proxy_set_header X-Real-IP $remote_addr;
}
```

### Separate `location` blocks per languages

```nginx
# PHP
location ~ \.php$ {
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}

# Python (uWSGI or Gunicorn via HTTP)
location ~ \.py$ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

# Node.js
location /node/ {
    proxy_pass http://127.0.0.1:3000;
}

```