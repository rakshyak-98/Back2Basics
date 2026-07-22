[[php error]] [[Nginx/Configuration]] [[Linux/commands/Services commands]]

# Apache modules

> Static (compiled-in) vs shared (dynamic `LoadModule`) — what you can toggle without recompiling httpd.

## Mental model

Apache **httpd** loads modules at startup. **Static modules** are baked into the binary — always present. **Shared modules** (`.so`) load via `LoadModule` in config. Only load what you need: fewer modules = smaller attack surface and memory.

```
httpd binary
  ├─ static modules (always on)
  └─ LoadModule mpm_event_module modules/mod_mpm_event.so
```

## Standard config / commands

### List compiled modules

```bash
apache2ctl -M          # Debian/Ubuntu
httpd -M               # RHEL
apachectl -t -D DUMP_MODULES
```

### Enable shared module (Debian)

```bash
sudo a2enmod rewrite ssl headers proxy proxy_http
sudo a2dismod mpm_prefork    # switch MPM carefully
sudo apachectl configtest
sudo systemctl reload apache2
```

### Typical production set

| Module | Purpose |
|--------|---------|
| `mpm_event` | Concurrent requests (with PHP-FPM, not prefork+mod_php) |
| `ssl` | TLS termination |
| `rewrite` | Pretty URLs |
| `headers` | Security headers |
| `proxy` + `proxy_http` | Reverse proxy to app |

### LoadModule line

```apache
LoadModule rewrite_module modules/mod_rewrite.so
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Invalid command 'RewriteRule'` | mod_rewrite loaded? | `a2enmod rewrite` |
| Apache won't start after enable | `apachectl configtest` | Fix LoadModule order; missing .so |
| PHP works, static 403 | Directory permissions | `Require all granted` + filesystem perms |
| SSL handshake fail | mod_ssl + cert paths | `SSLEngine on`; cert file readable |
| Proxy 502 | mod_proxy enabled | `a2enmod proxy proxy_http`; backend up |

## Gotchas

> [!WARNING]
> **MPM switch** — can't mix prefork/worker/event blindly; restart required; PHP-FPM pairs with event/worker.
>
> **Module loaded twice** — duplicate `LoadModule` lines break startup.
>
> **Distro splits packages** — `libapache2-mod-*` separate from core.

## When NOT to use

- Don't enable `mod_php` on new stacks — use [[PHP-FPM]] + proxy_fcgi or Nginx.
- Don't load debug modules (`mod_info`, `mod_status`) on public-facing servers without IP restrict.

## Related

[[php error]] [[PHP-FPM]] [[Nginx/Configuration]] [[Security/TLS (Transport Layer Security)]]
