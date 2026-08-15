[[ecosystem]] [[NodeJS]] [[Linux/commands/Services commands]]

# pm2

> Node.js process manager — keep apps alive, reload with zero-ish downtime, and supervise logs/clusters in production-like environments.

## Interview Relevance

Interviewers ask cluster mode vs fork, restart policies, and why pm2 is not a substitute for a proper init system on every host (but often pairs with systemd).

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

## Real-World Applications

Single VPS Node API: pm2 cluster behind Nginx; `pm2 save` after a good state.

**Example:** Memory leak — `max_memory_restart` in ecosystem file recycles the worker.

## Pros/Cons or Trade-offs

- **Pro:** Fast ops UX for Node on VMs.
- **Con:** Not a full orchestrator (K8s); sticky sessions need care in cluster mode.

## Comparison

- vs [[ecosystem]]: CLI ad-hoc vs declarative file.
- vs systemd alone: pm2 adds Node-aware clustering/log UX; systemd is the OS supervisor.

## Mistakes to Avoid

- Running `pm2` as a random user without `startup` integration then wondering why reboot kills apps.
- Cluster mode with in-memory sessions and no sticky/shared store.
- Ignoring log rotation until disks fill.
