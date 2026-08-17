[[services/systemd]] [[process]] [[system service unit files]] [[journalctl]]

# supervisorctl

> CLI for Supervisor — start/stop/tail programs from `supervisord.conf` when systemd is not the process manager.

```txt
        supervisorctl ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Legacy Python/deploy literacy: know Supervisor exists, how `reread`/`update` …

## Sources
- [Supervisor documentation](http://supervisord.org/) — deep-dive

## Key Concepts
- **Program stanzas:** command, directory, autostart, autorestart, log files.
- **reread + update:** pick up config changes without full restart of everything.
- **File logs vs journal:** Supervisor typically writes files; systemd uses [[journalctl]].
- **Not socket activation:** limited compared to systemd sockets/timers.


- **Core:** Supervisor is a Python process control system. `supervisorctl` talks to `supe…

## Technical Details
```ini
[program:web]
command=/var/www/venv/bin/gunicorn app:app
directory=/var/www
autostart=true
autorestart=true
stdout_logfile=/var/log/web.log
```

```bash
sudo supervisorctl status
sudo supervisorctl restart web
sudo supervisorctl tail -f web
sudo supervisorctl reread && sudo supervisorctl update
```

| Feature | Supervisor | systemd |
|---------|------------|---------|
| Socket activation | no | yes |
| Journal integration | file logs | journalctl |
| Dependency graph | limited | native |

## Mistakes to Avoid
- **Mistake:** Editing conf and forgetting `reread` + `update`
- **Mistake:** Running both systemd and Supervisor for the same app and fightin…
- **Mistake:** Assuming Supervisor logs appear in the journal by default

## Pros/Cons or Trade-offs
- **Pro:** Simple per-app process control without writing full unit files.
- **Con:** Extra daemon; weaker integration with boot targets and journal.

## Comparison
- vs [[services/systemd]]: prefer systemd on modern distros.
- vs [[tsp cli]]: tsp is ad-hoc batch; Supervisor is long-running program supervision.


### Use cases
- Restart a gunicorn worker pool on a legacy VM still running supervisord durin…
