[[Nginx]]

# nginx fastcgi

> nginx fastcgi — if you want nginx to handle other languages, you have two main routes.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** nginx fastcgi — if you want nginx to handle other languages, you have two main routes.

[fastcgi_module](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html#fastcgi_split_path_info)
if you want nginx to handle other languages, you have two main routes.

## Standard config / commands

```nginx
location ~ \.php$ {
    include fastcgi_params;
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 Bad Gateway | php-fpm socket down | `systemctl status php8.2-fpm`; socket path |
| File download instead of execute | missing `fastcgi_pass` | PHP must pass to FPM not `root` |
| PATH_INFO broken | split path info rules | Use documented `try_files` + fastcgi pattern |

---

## Gotchas

> [!WARNING]
> `SCRIPT_FILENAME` must be the **real filesystem path** PHP can open.

---

## When NOT to use

- Prefer php-fpm over legacy `mod_php` in Apache for isolation.


---

## Related

[[Nginx]]
