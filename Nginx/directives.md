server ->  defines a **virtual server**
- group all config block for a domain/port.

listen -> defines which IP/PORT this server listens on.

server_name ->
- is how Nginx decides which `server {...}` block should handle an incoming request.

root -> sets the base directory for serving static files.

index -> defines the default file to serve when a directory is requested.

location -> defines how to handle requests for a path

proxy_pass -> forwards requests to another server (reverse proxy).

proxy_set_header -> passes extra headers to the backend.
- Often used for `Host` `X-Real-IP` `X-Forward-For`

error_page -> defines a custom page for specific error codes.
- example `error_page 404 /custom_404.html;`

upstream -> defines a group of backend servers for load balancing.

gzip & gzip_types -> enable compression for responses.

```nginx
server {
	gzip on;
	gzip_types text/plain application/json;
}
```

auth_basic / auth_basic_user_file -> Enables HTTP basic authentication

```nginx
server {
	auth_basic "Restricted";
	auth_basic_user_file /etc/nginx/.htpasswd;
}
```

proxy_cache/proxy_cache_valid -> caches proxied responses

```nginx
proxy_cache my_cache;
proxy_cache_valid 200 1h;
```

> [!NOTE]
> Nginx directives are grouped by context (where they're allowed)
> `http {}` -> global HTTP settings.
> `server {}` -> per domain.
> `location {}` -> per path.
> `upstream {}` -> backend groups.

> [!INFO]
>  - When a request comes in, Nginx looks at the `Host` header (the domain part of the URL).
>  - It matches that value against the `server_name` in your config.
>  - If it matches, Nginx uses the `server {}` block to process the request.

> [!NOTE]
> if no `server_name` matches, Nginx falls back to the first `server {}` block for that port.
> Matching is case-insensitive.
> You can use regex, but wildcards are faster.
### Variants

**Wildcards** -> matches `foo.example.com`, `bar.example.com`
```ini
server_name *.example.com;
```

Multiple names
```ini
server_name example.com www.example.com;
```

Default server (catch-all)
```ini
server {
	listen 80 default_server;
	server_name;
}
```