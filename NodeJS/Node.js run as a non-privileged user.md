[[NodeJS]] [[CLI]] [[nvm]] [[Linux/commands/Services commands]]

# Node.js run as a non-privileged user

> One-line: never run app servers as root — bind high ports or use capabilities/setcap; delegate privileged ops to systemd; load nvm/env in service units explicitly.

## Mental model

Node apps should run as a **dedicated low-privilege user** (`node`, `app`, `www-data`). Root-owned processes that parse untrusted input are full box compromise on RCE. Privileged operations (reload nginx, bind :443) belong in **systemd** `ExecStartPre` or separate admin tools — not `sudo` from the app.

```
Bad:  root → node app.js (listening 3000)
Good: appuser → node app.js (3000) ──► reverse proxy (root binds 443)
Better: systemd User=appuser + EnvironmentFile + Restart=on-failure
```

Ports **< 1024** require root unless `setcap cap_net_bind_service` on the node binary (use sparingly) or a front proxy.

## Standard config / commands

### Interactive run as user

```bash
sudo -u appuser -H bash -lc 'cd /opt/myapp && node server.js'
# -H = target user's HOME (for .nvm, .env paths)
```

### With nvm

```bash
sudo -u appuser -H bash -lc 'cd /opt/myapp && source ~/.nvm/nvm.sh && nvm use && node server.js'
```

### systemd unit

```ini
[Unit]
Description=My Node App
After=network.target

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/myapp
EnvironmentFile=/opt/myapp/.env
ExecStart=/home/appuser/.nvm/versions/node/v22.16.0/bin/node server.js
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### File ownership

```bash
sudo useradd -r -s /bin/false appuser
sudo chown -R appuser:appuser /opt/myapp
# never run npm install as root in app dir then drop privileges — fix ownership
```

### Delegate nginx reload to systemd

```ini
# /etc/sudoers.d/app-deploy — prefer polkit/systemd timer over wide sudo
# Better: systemd path unit or `systemctl reload nginx` in deploy script as root
```

### Capabilities (avoid if possible)

```bash
sudo setcap 'cap_net_bind_service=+ep' $(readlink -f $(which node))
# document: lost on node upgrade/reinstall
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `EACCES` writing logs/uploads | File owner root | `chown` app dir to service user |
| `node: command not found` in service | PATH not loaded | Absolute path to node binary in unit |
| Env vars empty under systemd | Missing EnvironmentFile | Add `EnvironmentFile=`; no shell profile in services |
| Can't bind 80/443 | Privileged port | Proxy on 443; app on 3000+ |
| Permission denied on `npm install` | Running as wrong user | Install deps as appuser in CI/build stage |
| sudo nginx reload fails | NOPASSWD missing | Use root deploy hook, not app runtime sudo |

## Gotchas

> [!WARNING]
> **Build as root, run as user** — `node_modules` owned by root breaks runtime writes and native rebuilds.

> [!WARNING]
> **`setcap` on node** — any script run with that binary can bind low ports; prefer reverse proxy.

> [!WARNING]
> **Secrets in world-readable `.env`** — mode `600`, owned by service user.

## When NOT to use

- **One-shot CLI as your own user** — no need for service user locally.
- **Container** — USER directive in Dockerfile replaces host user model (still non-root).

## Related

[[CLI]] [[nvm]] [[Nginx/Configuration]] [[Linux/commands/Services commands]] [[Docker/Docker Runtime Security]]
