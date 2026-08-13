[[NodeJS]] [[npm command]] [[node modules]]

# node environment configuration

> Configure Node apps via env vars and files — `NODE_ENV`, secrets outside git, fail fast on missing required config.

---

## How it works

```txt
process.env.DATABASE_URL ← platform / dotenv (dev)
validate at boot → crash if required missing
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **NODE_ENV** | mode flag | “`production` enables optimizations / stricter.” |
| **dotenv** | Load `.env` file | “Dev convenience — not a secret store.” |
| **12-factor** | Config in env | “Same artifact, different env.” |


## Configuration and commands

```bash
export NODE_ENV=production
export DATABASE_URL=postgres://…
node app.js
```

```js
import 'dotenv/config' // local only
const url = process.env.DATABASE_URL
if (!url) throw new Error('DATABASE_URL required')
```

| Knob | Why it matters |
|------|----------------|
| Required vs optional | Boot fail vs defaults |
| Typed config module | Parse ints/bools once |
| Secrets manager | Prod — not flat `.env` in images |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Works on laptop only | Missing env in deploy | Set platform secrets |
| Wrong DB | Multiple `.env*` precedence | Document load order |
| `undefined` config | Typo in name | Central schema (zod/envalid) |
| Secret in git | `.env` committed | Rotate; gitignore; history purge |

---


## Gotchas

> [!WARNING]
> **Don’t bake secrets into Docker layers** — inject at runtime.

> [!WARNING]
> **`NODE_ENV=test` vs production** — frameworks change caching/error detail.

---


## When not to use

- **Putting all configuration in Redux/DB for static values** — environment/files are enough.
- **Client-side secret environment** — anything `NEXT_PUBLIC_` is public.

---


## Related

[[npm command]] [[expressjs]] [[Packages/Ajv (Another JSON validator)]]

## Sources

- [Wikipedia — node environment configuration](https://en.wikipedia.org/wiki/node_environment_configuration)
