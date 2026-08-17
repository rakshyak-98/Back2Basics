[[NodeJS]] [[NodeJS CLI]] [[node modules]] [[expressjs]] [[Packages/Ajv (Another JSON validator)]]

# node environment configuration

> Configure Node apps via env vars and files — `NODE_ENV`, secrets outside git, fail fast on missing required config.

```txt
        node environment c ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **node environment configuration** to check whether you can …

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

## Mistakes to Avoid
- **Mistake:** **Don’t bake secrets into Docker layers** — inject at runtime
- **Mistake:** **`NODE_ENV=test` vs production**
- **Mistake:** **Works on laptop only:** check Missing env in deploy
- **Mistake:** **Wrong DB:** check Multiple `.env*` precedence
- **Mistake:** **`undefined` config:** check Typo in name
- **Mistake:** **Secret in git:** check `.env` committed

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Configure Node apps via env vars and files — `NODE_ENV`, secrets outside git, fa…).
- **Con / when not:** **Putting all configuration in Redux/DB for static values…
- **Con / when not:** **Client-side secret environment**

## Comparison
- vs [[NodeJS CLI]]: know when each applies


### Use cases
- In production APIs and tooling, **node environment configuration** shows up w…
