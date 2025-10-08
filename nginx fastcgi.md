[fastcgi_module](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html#fastcgi_split_path_info)
if you want nginx to handle other languages, you have two main routes.

> [!NOTE]
> - Each language needs its own backend -> nginx does not interpret code.
> - PHP works because of PHP-FPM `php_fastcgi`. For others, you need a similar FastCGI handler or an HTTP reverse proxy.

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

### FastCGI configuration
`/etc/nginx/fastcgi.conf` -> the block define in here is part of Nginx + FastCGI configuration. It defines environment variables that Nginx sends to the FastCGI process (PHP-FPM).

- PHP (or any FastCGI backend) relies on certain CFI standard variables to understand the request.
- These lines explicitly pass HTTP request information from Nginx -> FastCGI.

|Line|Meaning|Example|
|---|---|---|
|`fastcgi_param QUERY_STRING $query_string;`|The URL query string after `?`|`/api.php?id=5` → `id=5`|
|`fastcgi_param REQUEST_METHOD $request_method;`|HTTP method|`GET`, `POST`, `PUT`, `DELETE`|
|`fastcgi_param CONTENT_TYPE $content_type;`|Request body type|`application/json`, `multipart/form-data`|
|`fastcgi_param CONTENT_LENGTH $content_length;`|Request body size in bytes|`123`|

> [!NOTE]
> - without them PHP would not know what query string, request method, or body type/length was.