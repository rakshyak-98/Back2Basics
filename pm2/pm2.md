[[ecosystem]] [[NodeJS]] [[Linux/commands/Services commands]]

# pm2

> Node.js process manager — keep apps alive, reload with zero-ish downtime, and supervise logs/clusters in production-like environments.

```txt
        pm2 ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask cluster mode vs fork, restart policies, and why pm2 is not a…

## Sources
- [PM2 documentation](https://pm2.keymetrics.io/docs/usage/quick-start/) — deep-dive

## Key Concepts
- **Managed processes:** start/stop/restart with names.
- **Cluster mode:** scale across CPU cores for stateless HTTP.
- **Reload:** rolling restart when app supports it.
- **Logs:** aggregated stdout/stderr per app.

## Technical Details
```bash
pm2 start npm --name api -- start
pm2 status
pm2 logs api
pm2 restart api
pm2 reload api
pm2 save && pm2 startup
```

| Command | Use |
|---------|-----|
| `start` | Launch |
| `reload` | Graceful rolling restart |
| `save`/`startup` | Resurrect after reboot |

## Mistakes to Avoid
- **Mistake:** Running `pm2` as a random user without `startup` integration the…
- **Mistake:** Cluster mode with in-memory sessions and no sticky/shared store
- **Mistake:** Ignoring log rotation until disks fill

## Pros/Cons or Trade-offs
- **Pro:** Fast ops UX for Node on VMs.
- **Con:** Not a full orchestrator (K8s); sticky sessions need care in cluster mode.

## Comparison
- vs [[ecosystem]]: CLI ad-hoc vs declarative file.
- vs systemd alone: pm2 adds Node-aware clustering/log UX; systemd is the OS supervisor.


### Use cases
- Single VPS Node API: pm2 cluster behind Nginx; `pm2 save` after a good state.

- **Example:** Memory leak
