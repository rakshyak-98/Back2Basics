[[NodeJS]] [[Packages/npm packages]] [[open api specification]] [[expressjs]]

# Ajv (Another JSON validator)

> Fast JSON Schema validator — compile a schema once, validate many payloads; get structured errors.

## Interview Relevance

Interviewers use **Ajv (Another JSON validator)** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **compile**, **JSON Schema**, **errors**.

## Sources

- [Ajv — JSON Schema validator](https://ajv.js.org/) — deep-dive
- [Wikipedia — Ajv](https://en.wikipedia.org/wiki/Ajv) — overview

## Key Concepts

- **compile:** Schema → function — Pay compile cost once.
- **JSON Schema:** Declarative contract — Share with OpenAPI often.
- **errors:** Why it failed — Map to 400 responses.

## Technical Details

```txt
schema → compile → validate(data) → true | errors[]
```

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

## Real-World Applications

In production APIs and tooling, **Ajv (Another JSON validator)** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Ajv major versions** — options and defaults changed; pin major; **Don’t trust client types alone** — still sanitize for XSS/SQL at use sites.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Fast JSON Schema validator — compile a schema once, validate many payloads; get …).
- **Con / when not:** **TypeScript-first DTOs** — zod/yup may fit better in TS apps.
- **Con / when not:** **Huge dynamic schemas per request** — compile cost dominates.

## Comparison

vs [[Packages/npm packages]]: know when each applies — do not treat them as interchangeable. vs [[open api specification]]: know when each applies — do not treat them as interchangeable. vs [[expressjs]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Ajv major versions** — options and defaults changed; pin major.
- **Don’t trust client types alone** — still sanitize for XSS/SQL at use sites.
- **format ignored:** check Missing ajv-formats; fix: Add plugin
- **Passes junk fields:** check No additionalProperties; fix: Set `false`
- **Slow validates:** check Recompiling each request; fix: Compile once at boot
- **Vague 400s:** check Dumping raw errors; fix: Map `instancePath` for clients
