[[NodeJS]] [[node environment configuration]] [[node package json]] [[CLI]]

# node-convict

> node-convict — loads config from defaults → file → environment variables → CLI args (order configurable). Each key has a schema: type, format, default, env var

```txt
        node-convict ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **node-convict** to see if you understand what it does ope…

## Sources
- [mozilla/node-convict](https://github.com/mozilla/node-convict) — deep-dive
- [Wikipedia — node-convict](https://en.wikipedia.org/wiki/node-convict) — overview

## Key Concepts
- **[node-convict](https://github.com/mozilla/node-convict) loads:** [node-convict](https://github.com/mozilla/node-convict) loads configuration f…
- **Validation runs:** Validation runs at startup


- **Core:** [node-convict](https://github.com/mozilla/node-convict) loads configuration f…

## Technical Details
- [node-convict](https://github.com/mozilla/node-convict) loads configuration f…
- Each key has a schema: type, format, default, environment variable name, docu…

```
defaults (in code)
    ↓ merge
config.json / config.toml
    ↓ merge
process.env (DATABASE_URL, PORT, …)
    ↓ validate
app.config.get('server.port')  → typed, validated
```

- Validation runs at startup

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

## Mistakes to Avoid
- **Mistake:** **Env vars are strings**
- **Mistake:** **Load order matters**
- **Mistake:** **Don't mutate config at runtime**
- **Mistake:** **App exits at boot with validation error:** check Stack trace n…
- **Mistake:** **Wrong value in prod:** check `config.getProperties()` log (red…
- **Mistake:** **`undefined` after load:** check Typo in nested path
- **Mistake:** **Secrets in logs:** check `sensitive: true` keys
- **Mistake:** **Unknown key ignored:** check `allowed: 'strict'` vs lax

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (node-convict — loads config from defaults → file → environment variables → CLI a…).
- **Con / when not:** **12-factor only environment, no files**
- **Con / when not:** **Dynamic configuration from control plane**
- **Con / when not:** **Secrets rotation mid-process**

## Comparison
- vs [[node environment configuration]]: know when each applies


### Use cases
- In production APIs and tooling, **node-convict** shows up whenever teams ship…
