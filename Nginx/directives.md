[[How does directive work#try_files]]

# directives

> directives — server — defines a virtual server

## Mental model

**Say it in one breath:** directives — server — defines a virtual server

server ->  defines a **virtual server**
- group all configuration block for a domain/port.
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

## Standard config / commands

See [[Configuration]] for full examples. Minimal server block:
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Wrong server block chosen | `server_name` mismatch; default_server | Check `nginx -T`; SNI and listen order |
| 404 on existing file | `root`/`alias` path wrong | `namei -l /path`; permissions for `www-data` |
| Proxy returns 502 | upstream down; bad `proxy_pass` URL | `curl` backend; trailing slash rules |
| Config test fails | typo in directive name | `nginx -t` shows file:line |

## Gotchas

> [!WARNING]
> `alias` replaces the matched location path — `root` appends the full URI.

## When NOT to use

- Do not put TLS certificates only in the default_server block if you serve many names.

## Related

[[How does directive work#try_files]]
