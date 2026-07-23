[[NodeJS]] [[node environment configuration]] [[node package json]]

# node-convict

> One-line: schema-validated config with env/JSON/file layering — fail fast at boot when a knob is missing or wrong type.

## Mental model

[node-convict](https://github.com/mozilla/node-convict) loads config from **defaults → file → environment variables → CLI args** (order configurable). Each key has a schema: type, format, default, env var name, doc string.

```
defaults (in code)
    ↓ merge
config.json / config.toml
    ↓ merge
process.env (DATABASE_URL, PORT, …)
    ↓ validate
app.config.get('server.port')  → typed, validated
```

Validation runs at startup — misconfigured deploy crashes immediately instead of corrupting prod data silently.

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| App exits at boot with validation error | Stack trace names key | Set env var or fix JSON; check `format` enum |
| Wrong value in prod | `config.getProperties()` log (redact sensitive) | Env var overrides file; check K8s secret mount |
| `undefined` after load | Typo in nested path | Use dot path exactly as schema |
| Secrets in logs | `sensitive: true` keys | Never `console.log` full config object |
| Unknown key ignored | `allowed: 'strict'` vs lax | Add to schema or fix typo in JSON |

## Gotchas

> [!WARNING]
> **Env vars are strings** — convict coerces via `format`; custom formats must parse `"false"`/`"0"` explicitly.

> [!WARNING]
> **Load order matters** — later sources win; document which file/env wins for on-call.

> [!WARNING]
> **Don't mutate config at runtime** — treat as immutable after validate except feature flags with clear lifecycle.

## When NOT to use

- **12-factor only env, no files** — lighter libs (`envalid`, `zod` + dotenv) may suffice.
- **Dynamic config from control plane** — need polling/consul/etcd, not static convict load-once.
- **Secrets rotation mid-process** — convict won't reload; use secret manager SDK.

## Related

[[node environment configuration]] [[node package json]] [[NodeJS]] [[CLI]]
