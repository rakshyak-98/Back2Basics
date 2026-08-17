[[NodeJS]] [[NodeJS CLI]] [[nvm]] [[Linux/commands/Services commands]] [[Nginx/Configuration]] [[Docker/Docker Runtime Security]]

# Node.js run as a non-privileged user

> Node.js run as a non-privileged user — node apps should run as a dedicated low-privilege user (node, app, www-data). Root-owned processes that parse untrusted input are

```txt
        Node.js run as a n ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Node.js run as a non-privileged user** to see if you und…

## Sources
- [Node.js — Security best practices](https://nodejs.org/en/learn/getting-started/security-best-practices) — deep-dive
- [Wikipedia — Node.js run as a non-privileged user](https://en.wikipedia.org/wiki/Node.js_run_as_a_non-privileged_user) — overview

## Key Concepts
- **Node apps:** Node apps should run as a **dedicated low-privilege user** (`node`, `app`, `w…
- **Ports:** <:** Ports **< 1024** require root unless `setcap cap_net_bind_service` on th…


- **Core:** Node apps should run as a **dedicated low-privilege user** (`node`, `app`, `w…

## Technical Details
- Node apps should run as a **dedicated low-privilege user** (`node`, `app`, `w…
- Root-owned processes that parse untrusted input are full box compromise on RC…
- Privileged operations (reload nginx, bind :443) belong in **systemd** `ExecSt…

```
Bad:  root → node app.js (listening 3000)
Good: appuser → node app.js (3000) ──► reverse proxy (root binds 443)
Better: systemd User=appuser + EnvironmentFile + Restart=on-failure
```

- Ports **< 1024** require root unless `setcap cap_net_bind_service` on the nod…

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

## Mistakes to Avoid
- **Mistake:** **Build as root, run as user**
- **Mistake:** **`setcap` on node**
- **Mistake:** **Secrets in world-readable `.env`**
- **Mistake:** **`EACCES` writing logs/uploads:** check File owner root
- **Mistake:** **`node: command not found` in service:** check PATH not loaded
- **Mistake:** **Env vars empty under systemd:** check Missing EnvironmentFile
- **Mistake:** **Can't bind 80/443:** check Privileged port
- **Mistake:** **Permission denied on `npm install`:** check Running as wrong u…
- **Mistake:** **sudo nginx reload fails:** check NOPASSWD missing

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node.js run as a non-privileged user — node apps should run as a dedicated low-p…).
- **Con / when not:** **One-shot CLI as your own user**
- **Con / when not:** **Container**

## Comparison
- vs [[NodeJS CLI]]: know when each applies


### Use cases
- In production APIs and tooling, **Node.js run as a non-privileged user** show…
