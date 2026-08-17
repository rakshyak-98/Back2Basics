[[apache command]] [[apache modules]] [[PHP-FPM]] [[Security/TLS (Transport Layer Security)]]

# Apache configurations

> Virtual hosts, document roots, and runtime user/group — where files are served from and which Linux identity httpd uses.

```txt
        Apache configurati ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask where to set `DocumentRoot`, how `AllowOverride` interacts w…

## Sources
- [Apache — VirtualHost Examples](https://httpd.apache.org/docs/current/vhosts/examples.html) — deep-dive
- [Apache — envvars (Debian)](https://manpages.debian.org/apache2) — overview

## Key Concepts
- **DocumentRoot:** filesystem path for the site → must match your app’s `public/` if you use one.
- **VirtualHost:** name/IP-based site containers → many sites per server.
- **Run user/group:** Debian `APACHE_RUN_USER`/`GROUP` (often `www-data`) → permission model.
- **`.htaccess` vs vhost:** per-directory overrides cost stat calls; prefer vhost in production.

## Technical Details
```bash
cat /etc/apache2/envvars
# export APACHE_RUN_USER=www-data
# export APACHE_RUN_GROUP=www-data

sudo a2enmod rewrite
sudo apache2ctl configtest
sudo systemctl restart apache2
```

- If the app lives at `/var/www/myproject/public`, `DocumentRoot` (and director…

| Symptom | Check | Fix |
|---------|-------|-----|
| 403 | Perms + `Require` | Fix ownership; `Require all granted` |
| Wrong site | `apache2ctl -S` | Fix vhost / ServerName |
| Rewrite ignored | `AllowOverride` / mod | Enable rewrite; allow FileInfo |

## Mistakes to Avoid
- **Mistake:** Serving the repo root (exposing `.env`)
- **Mistake:** Running httpd as root for content workers
- **Mistake:** Copying macOS/home paths into Linux vhosts

## Pros/Cons or Trade-offs
- **Pro:** `.htaccess` lets apps ship rewrite rules without vhost access.
- **Con:** `.htaccess` adds per-request overhead and scattered policy.

## Comparison
- vs Nginx server blocks: same vhost idea; different directive language.
- vs container sidecars: configuration still needs correct root and upstream to FPM/app.


### Use cases
- Laravel/Symfony-style apps: vhost `DocumentRoot` → `public/`, rewrite to `ind…

- **Example:** DocumentRoot left at `/var/www/html` after deploy to `/var/www/m…
