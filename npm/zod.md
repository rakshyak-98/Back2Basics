[[npm]] [[node package json]] [[expressjs]] [[open api specification]]

# zod

> TypeScript-first schema library — parse and validate untrusted data at runtime, then infer static types from the same schema.

```txt
        zod ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use Zod to check whether you validate at system boundaries (HTTP…

## Sources
- [Zod documentation](https://zod.dev/) — deep-dive
- [Zod GitHub repository](https://github.com/colinhacks/zod) — overview

## Key Concepts
- **Schema as source of truth:** one object describes validation and types → fewer drift bugs than separate in…
- **`parse` vs `safeParse`:** `parse` throws
- **Optional / default / nullable:** control missing vs null vs defaulted fields explicitly.
- **`refine` / `superRefine`:** cross-field rules (e.g. password confirmation) with custom issue paths.
- **Transforms:** coerce strings to numbers/dates carefully → document failure modes for bad in…


- **Core:** Zod defines schemas in TypeScript that both *validate* values at runtime (`pa…

## Technical Details
```js
import { z } from "zod";

const schema = z.object({
  description: z.string().max(500).optional(),
  images: z.array(z.string().url()).optional(),
  starRating: z.number().int().min(1).max(5).optional(),
  role: z.enum(["admin", "user", "guest"]).default("guest"),
});

type Form = z.infer<typeof schema>;

const authSchema = z
  .object({
    email: z.string().email(),
    password: z.string().min(8).optional(),
    confirmPassword: z.string().optional(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== undefined) {
      if (data.confirmPassword === undefined) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ["confirmPassword"],
          message: "Confirm password is required when setting a password",
        });
      } else if (data.password !== data.confirmPassword) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ["confirmPassword"],
          message: "Passwords do not match",
        });
      }
    }
  });
```

```js
const result = schema.safeParse(req.body);
if (!result.success) {
  return res.status(400).json(result.error.flatten());
}
// result.data is typed and validated
```

| Symptom | Likely cause |
|---------|--------------|
| Runtime type error after “valid” request | Validated a different object than you used |
| Always fail on dates | String vs `z.coerce.date()` mismatch |
| Empty object passes | Too many `.optional()` / missing `.strict()` |
| Huge error objects in logs | Logging full ZodError — prefer `flatten()` |

## Mistakes to Avoid
- **Mistake:** Believing compile-time types protect you from malformed JSON
- **Mistake:** Using `parse` in request handlers without a try/catch (prefer `s…
- **Mistake:** Encoding business workflow in schemas until they become unreadab…

## Pros/Cons or Trade-offs
- **Pro:** Single schema for types and runtime checks; excellent TypeScript ergonomics.
- **Con:** Bundle size and parse cost matter on hot paths — keep schemas at boundaries, not deep inside tight loops.
- **Con:** Complex `superRefine` logic can become hard to test if mixed with business rules.

## Comparison
- vs class-validator / Joi: Zod is TypeScript-native with inference
- vs OpenAPI-only generation: generated clients help clients


### Use cases
- Validate API request bodies, CLI flags, and environment configuration before …

- **Example:** An Express route `safeParse`s the body, returns 400 with field e…
