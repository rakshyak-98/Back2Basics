[[Nginx]] [[Configuration]]

# Nginx Automated Config Deployment

> One-line: CI/CD or app servers write configs to `/tmp`, validate, then sudo-copy into `sites-available` — never let unprivileged processes write directly to `/etc/nginx`.

## Mental model

Automated deploys (Node deploy scripts, Ansible, Terraform) generate per-tenant or per-release Nginx vhosts. The safe pattern:

```
App writes /tmp/site.conf  →  sudo nginx -t  →  sudo cp to sites-available  →  symlink  →  reload
```

Nginx reload is graceful (workers finish in-flight requests). **Always** `nginx -t` before reload — bad config can block new workers.

---

## Standard config / commands

### File ownership for static roots

```bash
sudo chown -R deploy-user:deploy-user /var/www/html
sudo chmod -R 755 /var/www/html
```

Nginx reads as `www-data`/`nginx` — world-readable static files are fine; writable only where uploads need it.

### Passwordless sudo for deploy user (visudo)

```bash
sudo visudo
```

```text
ubuntu ALL=(root) NOPASSWD: /usr/sbin/nginx -t
ubuntu ALL=(root) NOPASSWD: /bin/systemctl reload nginx
ubuntu ALL=(root) NOPASSWD: /bin/cp /tmp/nginx-*.conf /etc/nginx/sites-available/*
ubuntu ALL=(root) NOPASSWD: /bin/ln -sf /etc/nginx/sites-available/* /etc/nginx/sites-enabled/*
```

Verify least privilege:

```bash
sudo -l
```

### Deploy script pattern (Node)

```javascript
import { exec } from 'child_process';
import { writeFileSync } from 'fs';

const conf = generateNginxConf(domain, upstreamPort);
const tmpPath = `/tmp/nginx-${domain}.conf`;
const dest = `/etc/nginx/sites-available/${domain}`;

writeFileSync(tmpPath, conf);
await exec(`sudo cp ${tmpPath} ${dest}`);
await exec(`sudo ln -sf ${dest} /etc/nginx/sites-enabled/${domain}`);
await exec('sudo nginx -t');
await exec('sudo systemctl reload nginx');
```

> [!WARNING]
> Whitelist exact commands in sudoers — not blanket `NOPASSWD: ALL`.

### Rollback

```bash
sudo cp /etc/nginx/sites-available/site.conf.bak /etc/nginx/sites-available/site.conf
sudo nginx -t && sudo systemctl reload nginx
```

Keep previous config versioned in git or object storage.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Deploy succeeds but site 502 | Generated `proxy_pass` port wrong | Diff generated conf vs working; test upstream with `curl` |
| `nginx -t` fails in CI | Syntax error in template | Run `nginx -t` locally with same output; check unescaped `$` in templates |
| Permission denied on sudo | `sudo -l` | Add missing command to sudoers |
| Old config still served | Symlink not updated | `readlink -f /etc/nginx/sites-enabled/site`; force `ln -sf` |
| Include path broken | No shell expansion in `include` | Use absolute paths in generated configs |

---

## Gotchas

> [!WARNING]
> **Race on reload:** Two deploys concurrently can interleave copy + reload. Serialize deploys per host or use config hash + atomic rename.

> [!WARNING]
> **`envsubst` and `$uri`:** Template tools may eat Nginx `$variables`. Escape as `$uri` or use `$$uri` depending on tool.

> [!WARNING]
> **Never disable `nginx -t` in pipeline** — production incident from one missing semicolon.

---

## When NOT to use

- **Kubernetes ingress** — use Ingress controller or Gateway API; don't shell out to host Nginx from pods.
- **Multi-host fleet** — Ansible/Terraform managing `/etc/nginx` beats per-app sudo from runtime.

---

## Related

[[Configuration]] [[multi-domain]] [[nginx files]]
