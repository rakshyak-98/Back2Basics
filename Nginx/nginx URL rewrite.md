[[Nginx]]

# nginx URL rewrite

> nginx URL rewrite — what happens when user goes to /about

---

## How it works

|Nginx directive|What it actually does|When your browser URL becomes|Real folder on disk|
|---|---|---|---|
|`root /var/www/html;`|Physical folder|unchanged|`/var/www/html/blog/post1.html`|
|`alias`|Replace entire path|unchanged|something else|
|`try_files`|“Look here, then here, then fallback”|unchanged|multiple places|
|`rewrite`|**Changes the URL inside Nginx before it looks for files**|can change|depends|
|`return` / `proxy_pass`|Final answer|can change|doesn’t matter|


## Configuration and commands

```nginx
rewrite ^/old/(.*)$ /new/$1 permanent;
location /api/ {
    rewrite ^/api/(.*)$ /$1 break;
    proxy_pass http://backend;
}
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Redirect loop | `rewrite` plus `try_files` interaction | Test with `curl -I`; simplify rules |
| Query string dropped | rewrite without `$args` | Append `$is_args$args` when needed |
| 301 when expecting internal | `permanent` flag | Use `last` or `break` for internal rewrite |
| Wrong backend path | `proxy_pass` URI part | With URI in proxy_pass, location prefix is replaced |

---


## Gotchas

> [!WARNING]
> `rewrite ... permanent` sends **301** to the client — browser will cache it.

---


## When not to use

- Prefer `return 301` for simple host or scheme redirects — clearer than rewrite.


---


## Related

[[Nginx]]

## Sources

- [Wikipedia — nginx URL rewrite](https://en.wikipedia.org/wiki/nginx_URL_rewrite)
