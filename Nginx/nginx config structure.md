[[Configuration]] [[nginx files]] [[nginx fastcgi]] [[multi-domain]] [[directives]]

# nginx config structure

> Config tree — `nginx.conf` sets globals; `include` pulls sites, snippets, and params so each app has its own vhost file.





## Interview Relevance
Shows you know where to edit (main vs site vs snippet), how Debian `sites-enabled` differs from RHEL `conf.d`, and how to prove what is loaded with `nginx -T`.

## Sources
- [nginx.org — Configuring nginx](https://nginx.org/en/docs/beginners_guide.html) — overview
- [Debian Wiki — nginx](https://wiki.debian.org/Nginx) — overview
- [nginx.org — include](https://nginx.org/en/docs/ngx_core_module.html#include) — deep-dive

## Key Concepts
- **Main file:** `/etc/nginx/nginx.conf` — workers, gzip, logging, top-level `include`s.
- **Sites:** Debian-style `sites-available` + symlink in `sites-enabled`; available ≠ loaded.
- **Snippets / params:** Shared SSL, FastCGI, proxy header blocks; `*_params` files set common variables.
- **Includes:** Absolute paths preferred; no `~` expansion inside nginx config.

## Technical Details
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

| Symptom | Check | Fix |
|---------|-------|-----|
| Site not loading | Symlink missing | Enable in `sites-enabled` |
| Wrong vhost | `nginx -T` / `server_name` | Fix default_server clash |
| Include ignored | Path / glob | Absolute path; `*.conf` only |
| Module missing | `modules-enabled` | Install `libnginx-mod-*` |

## Real-World Applications
Add a new app by writing `sites-available/app`, symlinking into `sites-enabled`, testing, and reloading — without touching the global worker settings.

## Pros/Cons or Trade-offs
- **Pro:** Split vhosts keep blast radius small and reviews clear.
- **Con:** Distro layouts differ (Debian sites-* vs RHEL-heavy `conf.d/`) — muscle memory transfers poorly.

## Comparison
- vs one mega `nginx.conf`: structure scales; mega file does not.
- vs generated snippets: edit the template source, not hand-patched generated files.

## Mistakes to Avoid
- Leaving the default site stealing traffic for unknown hostnames.
- Assuming RHEL and Debian layouts are identical.
- Hand-editing generated snippets instead of regenerating from template.
