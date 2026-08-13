[[Nginx/Configuration]] [[nginx files]] [[nginx fastcgi]] [[/etc files]]

# nginx config structure

> Config tree — `nginx.conf` sets globals; `include` pulls sites, snippets, and params.

---

## How it works

```txt
/etc/nginx/nginx.conf
  ├── mime.types, modules-enabled/*
  ├── conf.d/*.conf
  ├── snippets/*
  └── sites-enabled/*  →  sites-available/*
```

| Piece | Edit for… |
|-------|-----------|
| `nginx.conf` | Workers, gzip, logging |
| `sites-available` + symlink | Per-domain `server {}` |
| `snippets/` | Shared SSL / FastCGI blocks |
| `*_params` | proxy / fastcgi / uwsgi headers |

---


## Configuration and commands

```nginx
# typical Debian http block ends with:
include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
```

```bash
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
sudo unlink /etc/nginx/sites-enabled/app
sudo nginx -t && sudo systemctl reload nginx
sudo nginx -T | grep -E 'server_name|include'
```

| Knob | Why it matters |
|------|----------------|
| `sites-enabled` only | Available ≠ loaded |
| `include` absolute paths | No `~` expansion |
| `fastcgi.conf` vs `fastcgi_params` | former sets `SCRIPT_FILENAME` |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Site not loading | Symlink missing | Enable in `sites-enabled` |
| Wrong vhost | `nginx -T` / `server_name` | Fix default_server clash |
| Include ignored | Path / glob | Absolute path; `*.conf` only |
| Module missing | `modules-enabled` | Install `libnginx-mod-*` |

---


## Gotchas

> [!WARNING]
> **Default site steals traffic** — disable `default` if unexpected hostnames hit it.

> [!WARNING]
> **RHEL uses `conf.d/` more; Debian uses sites-*** — know your distro layout.

---


## When not to use

- **One mega `nginx.conf` for many apps** — split vhosts.
- **Hand-editing generated snippets** — regenerate from template.

---


## Related

[[Nginx/Configuration]] [[nginx files]] [[nginx fastcgi]] [[multi-domain]]

## Sources

- [Wikipedia — nginx config structure](https://en.wikipedia.org/wiki/nginx_config_structure)
