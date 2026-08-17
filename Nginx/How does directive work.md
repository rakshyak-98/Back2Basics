[[Configuration]] [[Nginx internals]] [[nginx files]] [[web server]] [[directives]] [[nginx SPA deployment]]

# How Nginx directives work

> Directives live in context blocks — inheritance, merge rules, and phase order decide which `location` wins and what runs.





## Interview Relevance
Staff interviews probe whether you understand *why* a request hit the wrong `location`, how `try_files` interacts with `proxy_pass`, and why “`if` is evil” in Nginx.

## Sources
- [nginx.org — How nginx processes a request](https://nginx.org/en/docs/http/request_processing.html) — deep-dive
- [nginx.org — ngx_http_core_module (location)](https://nginx.org/en/docs/http/ngx_http_core_module.html#location) — deep-dive
- [nginx.org — If is evil](https://www.nginx.com/resources/wiki/start/topics/depth/ifisevil/) — overview

## Core Definition
A request is matched to a `server` by `listen` + `server_name`, then to a `location` by precedence rules; directives in that location (and inherited parents) run in Nginx’s HTTP phases.

## Key Concepts
- **Match pipeline:** request → `server_name` match → location (longest prefix / regex / exact) → directives (`try_files`, `proxy_pass`, …).
- **Exact / prefix / regex:** `=` highest; `^~` prefix stops regex search; `~`/`~*` regex; then general prefix.
- **`try_files`:** Checks filesystem paths in order, then falls back to a URI or named location — SPA and PHP front-controller pattern.
- **Inheritance:** Nested blocks inherit; duplicate directives in the same block — last wins; surprises across includes.

## Technical Details
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

```bash
sudo nginx -t
sudo systemctl reload nginx
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong location block | `nginx -T` full dump | More specific `location`; `^~` to skip regex |
| 404 static but file exists | `root` vs `alias` | `alias` strips location prefix; trailing slashes |
| PHP downloads not executes | `location ~ \.php$` + fastcgi | Include fastcgi_params; correct `SCRIPT_FILENAME` |
| Infinite redirect loop | `try_files` + rewrite | Remove conflicting rewrite |
| API 502 | `@backend` up? | `proxy_pass` URL trailing slash changes URI |
| Config change no effect | Reload vs restart | `nginx -t` first; check include path |

## Real-World Applications
SPA: `try_files $uri $uri/ /index.html`. PHP app: `try_files` then FastCGI. Static + API: specific `/api/` `location` before catch-all `/`.

## Pros/Cons or Trade-offs
- **Pro:** Declarative location tree is fast and predictable once you know precedence.
- **Con:** Misused `if` and nested regex locations become unmaintainable — prefer `map`, `try_files`, or split `server` blocks.

## Comparison
- vs [[directives]]: catalog of what each directive means vs how matching and inheritance work.
- vs [[nginx URL rewrite]]: rewrite changes URI mid-request; location selection happens first (and again after some rewrite flags).

## Mistakes to Avoid
- Using `if` for general programming in `location` — prefer `map`, `try_files`, or split server blocks.
- Ignoring `proxy_pass http://upstream/` trailing slash — strips location prefix; easy URI bug.
- Nesting many regex locations — consolidate with `map` or separate `server_name`s.
- Copying StackOverflow `if ($request_method = POST)` blocks without testing — subtle GET breakage.
