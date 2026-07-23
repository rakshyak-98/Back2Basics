[[Descriptive/doppler]] [[NodeJS/node-convict]] [[Terraform/variable file]] [[DevOps/Jenkins]]

# Pkl environment variable management

> Apple Pkl — typed config language that evaluates to JSON/YAML/properties — **env-specific config without stringly env soup**.

## Mental model

**Pkl** (.pkl files) describes configuration with **types, constraints, and composition**. Evaluator outputs formats for apps; **parameters** (e.g. `env=production`) select overlays at eval time — cleaner than duplicating `.env` files.

```
app.pkl + env prod.pkl/amends
        │
        ▼ pkl eval -p env=production
   JSON / YAML / properties → consumed by app / CI
```

| vs raw env vars | Pkl |
|-----------------|-----|
| Untyped strings | Typed fields + validation |
| Copy-paste per env | `amends` / imports compose configs |
| Secret leakage risk | Eval at deploy; integrate with secret stores |

## Standard config / commands

### Install CLI

```bash
# https://pkl-lang.org/main/current/pkl-cli/index.html
curl -L https://github.com/apple/pkl/releases/latest/download/pkl-linux-amd64 \
  -o /usr/local/bin/pkl && chmod +x /usr/local/bin/pkl
pkl --version
```

### Evaluate config

```bash
pkl eval app.pkl
pkl eval --format json app.pkl
pkl eval --format yaml app.pkl
pkl eval --format properties app.pkl   # java-style key=value
```

### Parameterize environment

```bash
pkl eval -p env=production app.pkl
pkl eval -p env=staging app.pkl
```

### Example `app.pkl`

```pkl
env: String = read?("env") ?? "development"

database {
  host = if (env == "production") "db.prod.internal" else "localhost"
  port = 5432
  poolSize = if (env == "production") 20 else 2
}

logLevel = if (env == "production") "info" else "debug"
```

### Compose configurations ([template docs](https://pkl-lang.org/main/current/language-tutorial/02_filling_out_a_template.html#composing-configurations))

```pkl
// prod.pkl
amends "app.pkl"
env = "production"
```

```bash
pkl eval prod.pkl
```

### REPL for exploration

```bash
pkl repl
# :load app.pkl
# database.host
```

### CI integration

```yaml
- run: pkl eval -p env=production --format json app.pkl > config.json
- run: ./deploy.sh config.json
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Eval error on field | Type/constraint violation | Fix Pkl types; don't coerce in app |
| Wrong env values | Parameter not passed | `-p env=…` in CI; default in Pkl |
| Secret in git | Password in `.pkl` | Externalize; amends + CI inject at eval |
| Drift prod vs staging | Duplicate keys | Single base + env amends files |
| App can't read output | Format mismatch | Match `--format json` to parser |

## Gotchas

> [!WARNING]
> **Pkl is not a secret store** — pair with [[Descriptive/doppler]] or vault for credentials; Pkl references env vars at eval time.

- **Eval in prod on every start** — cache rendered config or bake into image at build.
- **Team learning curve** — new DSL; document REPL workflow for onboarding.
- **Version pin** — pin Pkl CLI in CI for reproducible eval.

## When NOT to use

- Single static `config.json` with no env variance — overhead unjustified.
- Org already standardized on [[Terraform/variable file]] + tfvars for infra-only config.

## Related

[[Descriptive/doppler]] [[NodeJS/node-convict]] [[Terraform/variable file]] [[DevOps/Jenkins]]
