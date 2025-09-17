server_name -> is how Nginx decides which `server {...}` block should handle an incoming request.

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