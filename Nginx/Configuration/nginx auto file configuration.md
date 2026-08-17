[[Configuration]] [[multi-domain]] [[nginx files]] [[nginx config structure]]

# Nginx Automated Config Deployment

> Deploy scripts (Node, Ansible, Terraform) write vhost files — always `nginx -t`, then install, symlink, and reload so bad templates never take traffic.





## Interview Relevance
Platform interviews ask how you ship Nginx config safely: least-privilege sudo, atomic install, serialize reloads, and never skip config test in CI.

## Sources
- [nginx.org — Controlling nginx](https://nginx.org/en/docs/control.html) — overview
- [sudoers manual](https://www.sudo.ws/docs/man/1.8.27/sudoers.man/) — deep-dive
- [Ansible — template module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html) — overview

## Core Definition
Automated Nginx config deployment generates per-tenant or per-release vhost files, validates them with `nginx -t`, installs into the include tree, and gracefully reloads workers.

## Key Concepts
- **Safe pipeline:** write temp → `nginx -t` → install to `sites-available` → symlink `sites-enabled` → reload.
- **Graceful reload:** workers finish in-flight requests; bad config can block new workers if you skip the test.
- **Least-privilege sudo:** whitelist exact binaries/paths — not `NOPASSWD: ALL`.
- **Rollback:** keep previous conf versioned; restore + `nginx -t` + reload.

## Technical Details
```
App writes /tmp/site.conf  →  sudo nginx -t  →  sudo cp to sites-available  →  symlink  →  reload
```

### File ownership for static roots

```bash
sudo chown -R deploy-user:deploy-user /var/www/html
sudo chmod -R 755 /var/www/html
```

Nginx reads as `www-data`/`nginx` — world-readable static files are fine; writable only where uploads need it.

### Passwordless sudo for deploy user (visudo)

```text
ubuntu ALL=(root) NOPASSWD: /usr/sbin/nginx -t
ubuntu ALL=(root) NOPASSWD: /bin/systemctl reload nginx
ubuntu ALL=(root) NOPASSWD: /bin/cp /tmp/nginx-*.conf /etc/nginx/sites-available/*
ubuntu ALL=(root) NOPASSWD: /bin/ln -sf /etc/nginx/sites-available/* /etc/nginx/sites-enabled/*
```

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

Prefer testing before install in stricter pipelines: write → `nginx -t -c` test harness → copy → reload.

### Rollback

```bash
sudo cp /etc/nginx/sites-available/site.conf.bak /etc/nginx/sites-available/site.conf
sudo nginx -t && sudo systemctl reload nginx
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Deploy succeeds but site 502 | Generated `proxy_pass` port wrong | Diff generated conf vs working; `curl` upstream |
| `nginx -t` fails in CI | Syntax error in template | Reproduce locally; check unescaped `$` in templates |
| Permission denied on sudo | `sudo -l` | Add missing command to sudoers |
| Old config still served | Symlink not updated | `readlink -f …/sites-enabled/site`; force `ln -sf` |
| Include path broken | No shell expansion in `include` | Absolute paths in generated configs |

## Real-World Applications
Multi-tenant SaaS that provisions a vhost per customer domain from a deploy job; blue/green release that swaps upstream ports in generated config.

## Pros/Cons or Trade-offs
- **Pro:** Fast, repeatable vhost provisioning with graceful reload.
- **Con:** Concurrent deploys can race copy+reload — serialize per host or use atomic rename + single reload.
- **Con:** On Kubernetes, prefer Ingress/Gateway over shelling to host Nginx from pods.

## Comparison
- vs Ansible/Terraform fleet management: better for many hosts than per-app runtime sudo.
- vs [[Nginx ingress]]: in-cluster CRDs instead of writing `/etc/nginx` on nodes.

## Mistakes to Avoid
- Blanket `NOPASSWD: ALL` for the deploy user.
- Template tools (`envsubst`) eating Nginx `$uri` — escape (`$$uri`) as required.
- Disabling `nginx -t` in the pipeline “to save time.”
- Hand-editing generated files instead of the template source.
