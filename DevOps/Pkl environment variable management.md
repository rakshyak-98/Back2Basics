[[Descriptive/doppler]] [[NodeJS/node-convict]] [[Terraform/variable file]] [[Jenkins]] [[ecommerce-cicd-environments]]

# Pkl environment variable management

> Apple’s Pkl (pronounced “pickle”) is a typed configuration language — evaluate overlays per environment and emit JSON/YAML instead of maintaining a pile of untyped `.env` files.

```txt
        Pkl environment va ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers care less about Pkl trivia and more about whether you keep confi…

## Sources
- [Pkl documentation](https://pkl-lang.org/) — overview
- [Pkl language tutorial — basic configuration](https://pkl-lang.org/main/current/language-tutorial/01_basic_config.html) — deep-dive
- [Pkl CLI](https://pkl-lang.org/main/current/pkl-cli/index.html) — overview

## Key Concepts
- **Typed fields + validation:** catch bad values before deploy → fewer runtime surprises.
- **Composition:** base module + environment amends → one source of truth, not copy-paste files.
- **Parameters at eval:** `-p env=…` selects overlays in CI.
- **Output formats:** JSON, YAML, properties → match what the app already parses.
- **Not a secret store:** reference secrets from Doppler/vault at eval or inject later.


- **Core:** Pkl describes configuration with types, constraints, and composition (`amends…

## Technical Details
```
app.pkl + environment amends
        │
        ▼ pkl eval -p env=production
   JSON / YAML / properties → app / CI
```

| vs raw environment variables | Pkl |
|------------------------------|-----|
| Untyped strings | Typed fields + validation |
| Copy-paste per environment | `amends` / imports compose |
| Secret leakage risk | Eval at deploy; pair with secret stores |

```bash
curl -L https://github.com/apple/pkl/releases/latest/download/pkl-linux-amd64 \
  -o /usr/local/bin/pkl && chmod +x /usr/local/bin/pkl
pkl --version

pkl eval app.pkl
pkl eval --format json app.pkl
pkl eval --format yaml app.pkl
pkl eval -p env=production app.pkl
pkl eval -p env=staging app.pkl
```

```pkl
env: String = read?("env") ?? "development"

database {
  host = if (env == "production") "db.prod.internal" else "localhost"
  port = 5432
  poolSize = if (env == "production") 20 else 2
}

logLevel = if (env == "production") "info" else "debug"
```

```pkl
// production.pkl
amends "app.pkl"
env = "production"
```

```yaml
# CI
- run: pkl eval -p env=production --format json app.pkl > config.json
- run: ./deploy.sh config.json
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Eval error on field | Type/constraint violation | Fix Pkl types; do not coerce in the app |
| Wrong environment values | Parameter not passed | `-p env=…` in CI; default in module |
| Secret in git | Password in `.pkl` | Externalize; inject at eval |
| Drift across environments | Duplicate keys | Single base + amends files |
| App can't read output | Format mismatch | Match `--format` to parser |

## Mistakes to Avoid
- **Mistake:** Storing passwords in `.pkl` committed to git
- **Mistake:** Leaving the CLI unpinned in CI
- **Mistake:** Using Pkl for a single static `config.json` with no environment …
- **Mistake:** Silently coercing invalid values in the application after a fail…

## Pros/Cons or Trade-offs
- **Pro:** Types and composition catch configuration errors before runtime.
- **Con:** New DSL learning curve; document REPL (`pkl repl`) for onboarding.
- **Con:** Evaluating on every process start can be wasteful — bake or cache rendered output.

## Comparison
- vs raw `.env` / environment variables: Pkl adds types and composition
- vs [[NodeJS/node-convict]]: convict validates in-process Node configuration
- vs [[Terraform/variable file]]: tfvars for infrastructure


### Use cases
- CI evaluates `app.pkl` with `-p env=staging` or `production`, writes `config.…

- **Example:** Production and staging diverge because engineers duplicated keys
