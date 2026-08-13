[[services/systemd]] [[process]]

# supervisorctl

> Supervisor is a Python process control system — `supervisorctl` starts, stops, and tails logs for programs defined in `supervisord.conf` when systemd is not the chosen supervisor.

Common in legacy Python deployments. Modern Linux services prefer **systemd units** ([[system service unit files]]).

## Config sketch

```ini
[program:web]
command=/var/www/venv/bin/gunicorn app:app
directory=/var/www
autostart=true
autorestart=true
stdout_logfile=/var/log/web.log
```

## Control

```bash
sudo supervisorctl status
sudo supervisorctl restart web
sudo supervisorctl tail -f web
sudo supervisorctl reread && sudo supervisorctl update
```

## vs systemd

| Feature | Supervisor | systemd |
|---------|------------|---------|
| Socket activation | no | yes |
| Journal integration | file logs | [[journalctl]] |
| Dependency graph | limited | native |

## Related

[[services/systemd]] · [[process]]

## Sources

- [Supervisor documentation](http://supervisord.org/)
