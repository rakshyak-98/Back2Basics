[[NodeJS]] [[node environment configuration]] [[node package json]] [[CLI]]

# node-convict

> node-convict — loads config from defaults → file → environment variables → CLI args (order configurable). Each key has a schema: type, format, default, env var





## Interview Relevance
Interviewers probe **node-convict** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [mozilla/node-convict](https://github.com/mozilla/node-convict) — deep-dive
- [Wikipedia — node-convict](https://en.wikipedia.org/wiki/node-convict) — overview

## Core Definition
[node-convict](https://github.com/mozilla/node-convict) loads configuration from **defaults → file → environment variables → CLI arguments** (order configurable). Each key has a schema: type, format, default, environment variable name, document string.

## Key Concepts
- [node-convict](https://github.com/mozilla/node-convict) loads configuration from **defaults → file → environment variables → CLI arguments** (order configurable). Each key has a…
- Validation runs at startup — misconfigured deploy crashes immediately instead of corrupting production data silently.

## Technical Details
[node-convict](https://github.com/mozilla/node-convict) loads configuration from **defaults → file → environment variables → CLI arguments** (order configurable). Each key has a schema: type, format, default, environment variable name, document string.

```
defaults (in code)
    ↓ merge
config.json / config.toml
    ↓ merge
process.env (DATABASE_URL, PORT, …)
    ↓ validate
app.config.get('server.port')  → typed, validated
```

Validation runs at startup — misconfigured deploy crashes immediately instead of corrupting production data silently.

### Schema definition

```javascript
import convict from 'convict';

const config = convict({
  env: {
    doc: 'Application environment',
    format: ['production', 'development', 'test'],
    default: 'development',
    env: 'NODE_ENV',
  },
  server: {
    port: {
      doc: 'HTTP port',
      format: 'port',
      default: 3000,
      env: 'PORT',
    },
    host: {
      doc: 'Bind address',
      format: String,
      default: '0.0.0.0',
      env: 'HOST',
    },
  },
  db: {
    url: {
      doc: 'Database connection string',
      format: String,
      default: '',
      env: 'DATABASE_URL',
      sensitive: true,
    },
  },
});

config.loadFile('./config/production.json'); // optional per-env file
config.validate({ allowed: 'strict' });      // throw on unknown keys in strict mode

export default config;
```

### Usage

```javascript
import config from './config.js';

const port = config.get('server.port');
config.set('server.port', 8080); // runtime override (rare)
```

### Custom format

```javascript
convict.addFormat({
  name: 'non-empty-string',
  validate(val) {
    if (typeof val !== 'string' || !val.trim()) throw new Error('must be non-empty');
  },
});
```

### Export schema for ops

```javascript
console.log(config.toString()); // document all keys + env vars for runbooks
```

## Real-World Applications
In production APIs and tooling, **node-convict** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Env vars are strings** — convict coerces via `format`; custom formats must parse `"false"`/`"0"` explicitly; **Load order matters** — later sources win; document which file/env wins for on-call.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (node-convict — loads config from defaults → file → environment variables → CLI a…).
- **Con / when not:** **12-factor only environment, no files** — lighter libs (`envalid`, `zod` + dotenv) may suffice.
- **Con / when not:** **Dynamic configuration from control plane** — need polling/consul/etcd, not static convict load-once.
- **Con / when not:** **Secrets rotation mid-process** — convict won't reload; use secret manager SDK.

## Comparison
vs [[node environment configuration]]: know when each applies — do not treat them as interchangeable. vs [[node package json]]: know when each applies — do not treat them as interchangeable. vs [[CLI]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Env vars are strings** — convict coerces via `format`; custom formats must parse `"false"`/`"0"` explicitly.
- **Load order matters** — later sources win; document which file/env wins for on-call.
- **Don't mutate config at runtime** — treat as immutable after validate except feature flags with clear lifecycle.
- **App exits at boot with validation error:** check Stack trace names key; fix: Set env var or fix JSON; check `format` enum
- **Wrong value in prod:** check `config.getProperties()` log (redact sensitive); fix: Env var overrides file; check K8s secret mount
- **`undefined` after load:** check Typo in nested path; fix: Use dot path exactly as schema
- **Secrets in logs:** check `sensitive: true` keys; fix: Never `console.log` full config object
- **Unknown key ignored:** check `allowed: 'strict'` vs lax; fix: Add to schema or fix typo in JSON
