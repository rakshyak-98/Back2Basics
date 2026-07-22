[[NodeJS/node command]] [[Linux/supervisorctl]] [[Linux/commands/Services commands]]

# PM2 ecosystem file

> Declarative process config — cluster mode, env injection, logs, and restart policy for Node apps.

## Mental model

PM2 reads `ecosystem.config.js` (or `.cjs`/JSON) and starts one or more **apps**. Each app has script, instances, env, and restart rules. PM2 keeps processes alive, aggregates logs, and supports zero-downtime reload for cluster mode.

```
ecosystem.config.js → pm2 start → PM2 daemon → app workers
```

## Standard config / commands

### Production-ready ecosystem

```js
module.exports = {
  apps: [{
    name: 'booking-engine',
    script: './dist/index.js',       // not `npm start` in prod if avoidable
    instances: 'max',                // or number; use cluster for HTTP
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development',
    },
    env_production: {
      NODE_ENV: 'production',
      API_URL: 'https://api.example.com',
    },
    max_memory_restart: '512M',
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    merge_logs: true,
    time: true,
  }],
};
```

### Commands

```bash
pm2 start ecosystem.config.js --env production
pm2 reload ecosystem.config.js --env production   # zero-downtime cluster
pm2 save
pm2 startup                                       # systemd boot hook
pm2 logs booking-engine
pm2 monit
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| App not picking env | Wrong `--env` | `pm2 start --env production` |
| Restarts loop | `pm2 logs` | Fix crash; raise memory if OOM |
| `npm start` overhead | Script path | Point `script` at compiled JS |
| Cluster sticky sessions | Single instance or Redis adapter | Scale Socket.IO with adapter |
| Lost on reboot | `pm2 save` + startup | Re-run `pm2 startup` after PM2 upgrade |

## Gotchas

> [!WARNING]
> **Secrets in ecosystem file** — use env from host/secret manager, not committed values.
>
> **`instances: max` on CPU-bound** — can thrash; profile first.
>
> **PM2 + Docker** — usually one process per container; PM2 inside container is redundant unless legacy.

## When NOT to use

- Don't use PM2 inside Kubernetes — use Deployments + probes.
- Don't cluster non-HTTP workers (queue consumers) without idempotency — use fixed instance count.

## Related

[[NodeJS/clustering]] [[Linux/supervisorctl]] [[npm/npm script]] [[Deployment/vercel cli]]
