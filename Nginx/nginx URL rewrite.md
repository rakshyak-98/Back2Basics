[[URL Rewriting]] [[Configuration]] [[How does directive work]] [[nginx SPA deployment]]

# nginx URL rewrite

> Change the URI inside Nginx before looking up files or proxying — different from `root`/`alias`/`try_files`, which leave the browser URL alone unless you `return`/`permanent`.





## Interview Relevance
Interviewers distinguish internal rewrite vs external redirect (`permanent`/`redirect`), query-string handling, and interaction with `proxy_pass`.

## Sources
- [nginx.org — ngx_http_rewrite_module](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html) — deep-dive
- [nginx.org — Creating NGINX Rewrite Rules](https://www.nginx.com/blog/creating-nginx-rewrite-rules/) — overview

## Key Concepts
| Nginx directive | What it does | Browser URL | Disk / upstream |
|-----------------|--------------|-------------|-----------------|
| `root` | Physical folder base | unchanged | URI under root |
| `alias` | Replace location prefix | unchanged | different path |
| `try_files` | Try paths then fallback | unchanged | multiple places |
| `rewrite` | Change URI inside Nginx | can change if redirect flag | depends |
| `return` / `proxy_pass` | Final answer / proxy | can change | N/A |

- **Flags:** `last` re-search locations; `break` stop rewrite module; `redirect` (302); `permanent` (301).
- **Query string:** Rewrite may drop `$args` unless you append `$is_args$args`.

## Technical Details
```nginx
rewrite ^/old/(.*)$ /new/$1 permanent;
location /api/ {
    rewrite ^/api/(.*)$ /$1 break;
    proxy_pass http://backend;
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Redirect loop | `rewrite` plus `try_files` interaction | Test with `curl -I`; simplify rules |
| Query string dropped | rewrite without `$args` | Append `$is_args$args` when needed |
| 301 when expecting internal | `permanent` flag | Use `last` or `break` for internal rewrite |
| Wrong backend path | `proxy_pass` URI part | With URI in proxy_pass, location prefix is replaced |

## Real-World Applications
Migrate `/old/...` to `/new/...` with 301; strip `/api` prefix before proxying to a backend that expects bare paths.

## Pros/Cons or Trade-offs
- **Pro:** Powerful pattern-based URI transforms without touching the app.
- **Con:** Long rewrite chains are hard to debug — prefer `return` for simple redirects.

## Comparison
- vs [[URL Rewriting]]: general concept vs Nginx `rewrite`/`return` specifics.
- vs `return 301`: clearer for host/scheme redirects than complex rewrite.

## Mistakes to Avoid
- Using `rewrite ... permanent` when you only needed an internal rewrite — browsers cache 301s.
- Preferring rewrite for simple redirects instead of `return 301`.
- Chaining rewrites that fight `try_files` SPA fallbacks.
