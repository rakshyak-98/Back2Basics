[[NodeJS]] [[Packages/npm packages]] [[open api specification]]

# Ajv (Another JSON validator)

> Fast JSON Schema validator — compile a schema once, validate many payloads; get structured errors.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `ajv.compile(schema)` returns a validate function; call it on each request body; on failure read `validate.errors`.

```txt
schema → compile → validate(data) → true | errors[]
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **compile** | Schema → function | “Pay compile cost once.” |
| **JSON Schema** | Declarative contract | “Share with OpenAPI often.” |
| **errors** | Why it failed | “Map to 400 responses.” |

## Standard config / commands

```js
import Ajv from 'ajv'
const ajv = new Ajv()
const validate = ajv.compile({
  type: 'object',
  properties: {
    name: { type: 'string' },
    age: { type: 'integer', minimum: 18 },
    email: { type: 'string', format: 'email' },
  },
  required: ['name', 'email'],
  additionalProperties: false,
})

if (!validate(data)) console.log(validate.errors)
```

```bash
npm install ajv
```

| Knob | Why it matters |
|------|----------------|
| `additionalProperties: false` | Reject unknown fields |
| `allErrors` | Collect every failure |
| Formats plugin | `format: email` needs ajv-formats |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| format ignored | Missing ajv-formats | Add plugin |
| Passes junk fields | No additionalProperties | Set `false` |
| Slow validates | Recompiling each request | Compile once at boot |
| Vague 400s | Dumping raw errors | Map `instancePath` for clients |

---

## Gotchas

> [!WARNING]
> **Ajv major versions** — options and defaults changed; pin major.

> [!WARNING]
> **Don’t trust client types alone** — still sanitize for XSS/SQL at use sites.

---

## When NOT to use

- **TypeScript-first DTOs** — zod/yup may fit better in TS apps.
- **Huge dynamic schemas per request** — compile cost dominates.

---

## Related

[[Packages/npm packages]] [[expressjs]] [[open api specification]]
