[[Nginx/Configuration]] [[Nginx/nginx internals]] [[Nginx/How does directive work]]

# How Nginx directives work

> Directives in context blocks compose request handling — inheritance, merge rules, and phase order determine which `location` wins.

## Mental model

Config is hierarchical: `main` → `events` → `http` → `server` → `location`. Directives inherit downward unless overridden. **`location`** matching uses prefix, regex (`~`), and priority (`=`, `^~`). **`try_files`** walks filesystem then named location. **`proxy_pass`** forwards to upstream. Order of **processing phases** (not file order) matters for rewrite vs access.

```
request → server_name match → location longest prefix / regex → directives (try_files, proxy_pass, …)
```

## Standard config / commands

### PHP front controller

```nginx
location / {
    try_files $uri $uri/ /index.php?$query_string;
}
```

### Named fallback upstream

```nginx
location / {
    try_files $uri $uri/ @backend;
}

location @backend {
    proxy_pass http://127.0.0.1:3000;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}
```

### Prefix vs regex priority

```nginx
location = /exact { ... }           # highest: exact
location ^~ /static/ { ... }        # prefix, stop regex search
location ~ \.php$ { ... }           # case-sensitive regex
location / { ... }                   # general prefix
```

### Validate and reload

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong location block | `nginx -T` full dump | More specific `location`; `^~` to skip regex |
| 404 static but file exists | `root` vs `alias` | `alias` strips location prefix; trailing slashes |
| PHP downloads not executes | `location ~ \.php$` + fastcgi | Include fastcgi_params; correct `SCRIPT_FILENAME` |
| Infinite redirect loop | `try_files` + rewrite | Remove conflicting rewrite |
| API 502 | `@backend` up? | `proxy_pass` URL trailing slash changes URI |
| Config change no effect | Reload vs restart | `nginx -t` first; check include path |

## Gotchas

> [!WARNING]
> **`if` is evil** in location — use `map`, `try_files`, or split server blocks.
>
> **`proxy_pass http://upstream/` trailing slash** — strips location prefix; easy URI bug.
>
> **Duplicate directives** — last wins in same block; inheritance surprises across nested blocks.

## When NOT to use

- Don't copy StackOverflow `if ($request_method = POST)` blocks without testing — subtle break GET.
- Don't nest ten regex locations — consolidate with `map` or separate server names.

## Related

[[Nginx/Configuration]] [[Nginx/nginx files]] [[Nginx/web server]] [[php error]]
