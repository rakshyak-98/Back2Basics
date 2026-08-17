[[NodeJS]] [[Packages/npm packages]] [[open api specification]] [[expressjs]]

# Ajv (Another JSON validator)

> Fast JSON Schema validator — compile a schema once, validate many payloads; get structured errors.

```txt
        Ajv (Another JSON  ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **Ajv (Another JSON validator)** to check whether you can ex…

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

## Mistakes to Avoid
- **Mistake:** **Ajv major versions** — options and defaults changed; pin major
- **Mistake:** **Don’t trust client types alone**
- **Mistake:** **format ignored:** check Missing ajv-formats; fix: Add plugin
- **Mistake:** **Passes junk fields:** check No additionalProperties
- **Mistake:** **Slow validates:** check Recompiling each request
- **Mistake:** **Vague 400s:** check Dumping raw errors

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Fast JSON Schema validator — compile a schema once, validate many payloads; get …).
- **Con / when not:** **TypeScript-first DTOs**
- **Con / when not:** **Huge dynamic schemas per request**

## Comparison
- vs [[Packages/npm packages]]: know when each applies


### Use cases
- In production APIs and tooling, **Ajv (Another JSON validator)** shows up whe…
