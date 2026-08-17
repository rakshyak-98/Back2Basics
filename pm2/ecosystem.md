[[pm2]] [[NodeJS]]

# PM2 ecosystem file

> Declarative process config (`ecosystem.config.js`) — apps, instances, environment variables, log paths, and restart policies in one reviewable file.

```txt
        PM2 ecosystem file ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers prefer ecosystem files over tribal `pm2 start` commands

## Sources
- [PM2 — Ecosystem file](https://pm2.keymetrics.io/docs/usage/application-declaration/) — deep-dive

## Key Concepts
- **`apps` array:** one or more processes.
- **`instances` / `exec_mode`:** `cluster` vs `fork`.
- **`env` / `env_production`:** environment-specific variables.
- **Restart rules:** `max_restarts`, `max_memory_restart`, watch (usually off in prod).

## Technical Details
```js
module.exports = {
  apps: [{
    name: "api",
    script: "dist/server.js",
    instances: "max",
    exec_mode: "cluster",
    env_production: { NODE_ENV: "production" },
    max_memory_restart: "500M",
    error_file: "./logs/api-err.log",
    out_file: "./logs/api-out.log",
  }],
};
```

```bash
pm2 start ecosystem.config.js --env production
pm2 reload ecosystem.config.js --env production
```

## Mistakes to Avoid
- **Mistake:** Committing production secrets in `env`
- **Mistake:** `instances: max` on a tiny VM sharing the box with DB
- **Mistake:** Forgetting `--env production` and booting with dev defaults

## Pros/Cons or Trade-offs
- **Pro:** Git-reviewed process shape; repeatable deploys.
- **Con:** Secrets still need injection (not plaintext in git).

## Comparison
- vs ad-hoc [[pm2]] CLI: file is source of truth.
- vs Docker Compose: similar declarative idea at process vs container layer.


### Use cases
- Same file for API + worker with different scripts and instance counts.

- **Example:** Enable `watch: true` in production by mistake
