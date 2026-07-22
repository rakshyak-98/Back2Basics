[[systemd]] [[Services commands]] [[process]] [[Linux application management]]

# supervisorctl

> One-line: **Supervisord process control** — keep worker processes (Celery, gunicorn, custom daemons) alive when systemd units aren't the chosen layer. `reread` vs `update` trips everyone once.

## Mental model

**Supervisord** is a parent daemon that spawns children, restarts on crash, and rotates logs. Config lives in `/etc/supervisor/conf.d/*.conf`. Changes on disk are **not** live until `reread` + `update`. Unlike systemd, one supervisord tree is typical per machine/container.

```
supervisord (PID 1 or child)
  ├── program:celery_worker
  ├── program:gunicorn
  └── group:web (optional)
supervisorctl → UNIX socket → supervisord
```

| Command | Effect |
|---------|--------|
| `reread` | Reload config files; report new/changed programs |
| `update` | Apply changes (start/stop/restart as needed) |
| `start/stop/restart <name>` | Target one program or group |
| `status` | RUNNING / STOPPED / FATAL |
| `tail -f <name> stdout` | Stream logs |

## Standard config / commands

**Minimal program stanza:**

```ini
; /etc/supervisor/conf.d/celery.conf
[program:celery_worker]
command=/opt/venv/bin/celery -A myapp worker -l info
directory=/opt/myapp
user=appuser
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker.err
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
environment=PATH="/opt/venv/bin",DJANGO_SETTINGS_MODULE="myapp.settings"
```

**Apply workflow (always this order):**

```bash
sudo supervisorctl reread          # "celery_worker: available"
sudo supervisorctl update          # starts new/changed
sudo supervisorctl status
sudo supervisorctl restart celery_worker
sudo supervisorctl tail -f celery_worker stderr
```

**Groups:**

```ini
[group:web]
programs=gunicorn,celery_worker
priority=999
```

```bash
sudo supervisorctl restart web:*
```

**Socket / CLI config** (`/etc/supervisor/supervisord.conf`):

```ini
[unix_http_server]
file=/var/run/supervisor.sock
chmod=0700

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| FATAL / backoff | `supervisorctl tail celery_worker stderr` | Fix command path; venv; permissions |
| Config change ignored | Ran only `restart` | `reread` then `update` |
| RUNNING but not working | Port bind; wrong `directory` | `ss -lntp`; fix `user` and cwd |
| Zombie children | Missing `stopasgroup` | Add `stopasgroup=true`, `killasgroup=true` |
| Can't connect to socket | supervisord down | `systemctl status supervisor`; start service |
| Log disk full | `stdout_logfile_maxbytes` | Set rotation; logrotate |
| Duplicate processes | Two supervisord instances | One config root; check Docker vs host |

## Gotchas

> [!WARNING]
> **`autorestart=true` on migration scripts** — restart loop hammers DB. Use `autostart=false`, `startsecs=10`, or `exitcodes=0`.

> [!WARNING]
> **Running supervisord as PID 1 in Docker** — need `tini` or `--nodaemon` patterns; zombie reaping breaks without init.

- **systemd vs supervisor** — pick one orchestration layer per app; don't double-wrap same process.
- **`user=`** — must exist before start; file permissions must allow that user.
- **Environment** — doesn't load login shell; set `environment=` explicitly.

## When NOT to use

- **Modern fleet on systemd** — native units + `Restart=always` often suffice; less moving parts.
- **Kubernetes** — use Deployments, not supervisord inside container (unless legacy image).
- **One-shot batch jobs** — use cron/systemd timer, not autorestart supervisor.

## Related

[[systemd]] [[Services commands]] [[process]] [[Linux application management]] [[crontab]]
