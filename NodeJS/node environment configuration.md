[[NodeJS]] [[npm command]] [[node modules]] [[expressjs]] [[Packages/Ajv (Another JSON validator)]]

# node environment configuration

> Configure Node apps via env vars and files — `NODE_ENV`, secrets outside git, fail fast on missing required config.





## Interview Relevance
Interviewers use **node environment configuration** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **NODE_ENV**, **dotenv**, **12-factor**.

## Sources
- [Node.js — process.env](https://nodejs.org/api/process.html#processenv) — overview
- [Wikipedia — node environment configuration](https://en.wikipedia.org/wiki/node_environment_configuration) — overview

## Key Concepts
- **NODE_ENV:** mode flag — `production` enables optimizations / stricter.
- **dotenv:** Load `.env` file — Dev convenience — not a secret store.
- **12-factor:** Config in env — Same artifact, different env.

## Technical Details
```txt
process.env.DATABASE_URL ← platform / dotenv (dev)
validate at boot → crash if required missing
```

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

## Real-World Applications
In production APIs and tooling, **node environment configuration** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Don’t bake secrets into Docker layers** — inject at runtime; **`NODE_ENV=test` vs production** — frameworks change caching/error detail.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Configure Node apps via env vars and files — `NODE_ENV`, secrets outside git, fa…).
- **Con / when not:** **Putting all configuration in Redux/DB for static values** — environment/files are enough.
- **Con / when not:** **Client-side secret environment** — anything `NEXT_PUBLIC_` is public.

## Comparison
vs [[npm command]]: know when each applies — do not treat them as interchangeable. vs [[node modules]]: know when each applies — do not treat them as interchangeable. vs [[expressjs]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Don’t bake secrets into Docker layers** — inject at runtime.
- **`NODE_ENV=test` vs production** — frameworks change caching/error detail.
- **Works on laptop only:** check Missing env in deploy; fix: Set platform secrets
- **Wrong DB:** check Multiple `.env*` precedence; fix: Document load order
- **`undefined` config:** check Typo in name; fix: Central schema (zod/envalid)
- **Secret in git:** check `.env` committed; fix: Rotate; gitignore; history purge
