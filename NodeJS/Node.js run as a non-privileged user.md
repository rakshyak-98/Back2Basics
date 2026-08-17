[[NodeJS]] [[CLI]] [[nvm]] [[Linux/commands/Services commands]] [[Nginx/Configuration]] [[Docker/Docker Runtime Security]]

# Node.js run as a non-privileged user

> Node.js run as a non-privileged user — node apps should run as a dedicated low-privilege user (node, app, www-data). Root-owned processes that parse untrusted input are





## Interview Relevance
Interviewers probe **Node.js run as a non-privileged user** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [Node.js — Security best practices](https://nodejs.org/en/learn/getting-started/security-best-practices) — deep-dive
- [Wikipedia — Node.js run as a non-privileged user](https://en.wikipedia.org/wiki/Node.js_run_as_a_non-privileged_user) — overview

## Core Definition
Node apps should run as a **dedicated low-privilege user** (`node`, `app`, `www-data`). Root-owned processes that parse untrusted input are full box compromise on RCE. Privileged operations (reload nginx, bind :443) belong in **systemd** `ExecStartPre` or separate administrator tools — not `sudo` from the application.

## Key Concepts
- Node apps should run as a **dedicated low-privilege user** (`node`, `app`, `www-data`). Root-owned processes that parse untrusted input are full box compromise on RCE. Privilege…
- Ports **< 1024** require root unless `setcap cap_net_bind_service` on the node binary (use sparingly) or a front proxy.

## Technical Details
Node apps should run as a **dedicated low-privilege user** (`node`, `app`, `www-data`). Root-owned processes that parse untrusted input are full box compromise on RCE. Privileged operations (reload nginx, bind :443) belong in **systemd** `ExecStartPre` or separate administrator tools — not `sudo` from the application.

```
Bad:  root → node app.js (listening 3000)
Good: appuser → node app.js (3000) ──► reverse proxy (root binds 443)
Better: systemd User=appuser + EnvironmentFile + Restart=on-failure
```

Ports **< 1024** require root unless `setcap cap_net_bind_service` on the node binary (use sparingly) or a front proxy.

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

## Real-World Applications
In production APIs and tooling, **Node.js run as a non-privileged user** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Build as root, run as user** — `node_modules` owned by root breaks runtime writes and native rebuilds; **`setcap` on node** — any script run with that binary can bind low ports; prefer reverse proxy.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node.js run as a non-privileged user — node apps should run as a dedicated low-p…).
- **Con / when not:** **One-shot CLI as your own user** — no need for service user locally.
- **Con / when not:** **Container** — USER directive in Dockerfile replaces host user model (still non-root).

## Comparison
vs [[CLI]]: know when each applies — do not treat them as interchangeable. vs [[nvm]]: know when each applies — do not treat them as interchangeable. vs [[Linux/commands/Services commands]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Build as root, run as user** — `node_modules` owned by root breaks runtime writes and native rebuilds.
- **`setcap` on node** — any script run with that binary can bind low ports; prefer reverse proxy.
- **Secrets in world-readable `.env`** — mode `600`, owned by service user.
- **`EACCES` writing logs/uploads:** check File owner root; fix: `chown` app dir to service user
- **`node: command not found` in service:** check PATH not loaded; fix: Absolute path to node binary in unit
- **Env vars empty under systemd:** check Missing EnvironmentFile; fix: Add `EnvironmentFile=`; no shell profile in services
- **Can't bind 80/443:** check Privileged port; fix: Proxy on 443; app on 3000+
- **Permission denied on `npm install`:** check Running as wrong user; fix: Install deps as appuser in CI/build stage
- **sudo nginx reload fails:** check NOPASSWD missing; fix: Use root deploy hook, not app runtime sudo
