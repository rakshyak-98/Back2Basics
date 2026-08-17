[[apache modules]] [[apache configurations]] [[Linux/commands/Services commands]]

# Apache commands

> Distro helpers and `apachectl`/`apache2ctl` — enable modules/sites, configtest, and graceful reload without guessing file paths.





## Interview Relevance
Interviewers expect Debian `a2enmod`/`a2ensite` fluency and the habit of `configtest` before reload.

## Sources
- [Debian Wiki — Apache](https://wiki.debian.org/Apache) — overview
- [Apache HTTP Server — apachectl](https://httpd.apache.org/docs/current/programs/apachectl.html) — deep-dive

## Key Concepts
- **`a2enmod` / `a2dismod`:** symlink module configs on Debian/Ubuntu.
- **`a2ensite` / `a2dissite`:** enable virtual hosts.
- **`apache2ctl` / `httpd`:** control + dump modules/config.
- **Graceful reload:** finish old requests when configuration is valid.

## Technical Details
```bash
sudo a2enmod rewrite ssl headers proxy proxy_http
sudo a2ensite myapp.conf
sudo apache2ctl configtest
sudo systemctl reload apache2

apache2ctl -M          # loaded modules
apache2ctl -S          # vhost map
```

`a2enmod rewrite` enables `mod_rewrite` for clean URLs (`/blog/title` → `index.php?…`).

| Task | Command |
|------|---------|
| Enable module | `a2enmod <name>` |
| Disable module | `a2dismod <name>` |
| Test config | `apache2ctl configtest` |
| Reload | `systemctl reload apache2` |

## Real-World Applications
First steps on a fresh Ubuntu image: enable `rewrite` + `ssl`, point a vhost at `/var/www/…/public`, configtest, reload.

**Example:** `Invalid command 'RewriteRule'` — module not enabled; `a2enmod rewrite` then reload.

## Pros/Cons or Trade-offs
- **Pro:** Distro tools beat hand-editing `mods-enabled` symlinks.
- **Con:** RHEL paths differ (`httpd`, no `a2enmod`) — know both.

## Comparison
- vs editing `httpd.conf` only: helpers reduce path mistakes on Debian.
- vs [[Nginx]] `-t` + reload: same safety pattern, different binary.

## Mistakes to Avoid
- Reloading without `configtest`.
- Enabling modules you do not need (attack surface).
- Assuming `a2enmod` exists on every distro.
