[[npm]]

# zod

> zod — message: 'Confirm password is required when setting a password',

---

## Mental model

**Say it in one breath:** zod — I can explain the job, the configuration, and the top failure without jargon.


Making field options
```js
cosnt schema = z.object({
	descriptino: z.string().max(500).optionl(),
	images: z.array(z.string()).url().optionl();
	starRating: z.number().int().min(1).max(5).optionl(),
})
```
Default values
```js
const schema = z.object({
	role: z.enum(["admin", "user", "guest"]).default("guest"),
	theme: z.enum(["light", "dark"]).default("guest").optional().default("light"),
})
```
`superRefine` and `refine`
```js
const authSchema = z.object({
	email: z.string().email(),
	password: z.string().min(8).optional(),
	confirmPassword: z.string().optional(),
}).superRefine((data, ctx) => {
	if (data.password !== undefined){
		if(data.confirmPassword === undefined){
			ctx.addIssue({
				code: z.ZodIssueCode.invalid_type,
				expected: 'string',
				received: 'undefined',
				path: ['confirmPassword'],
				message: 'Confirm password is required when setting a password',
			});
		} else if (data.password !== data.confirmPassword){
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				path: ['confirmPassword'],
				message: 'Password do not match',
			})
		}
	}
})
```
```js
const contactSchema = z.object({
  email: z.string().email().optional(),
  phone: z.string().regex(/^\+

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **zod** | This note’s core idea | “I explain zod in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

---

## Standard config / commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Runtime error | stack / overlay | Null-check; fix import |
| Build fail | deps / tsconfig | Align versions; clear cache |
| Auth/CORS | network tab | Headers and tokens |

---

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---

## When NOT to use

- Skip when a simpler existing approach already fits.

---

## Related

[[npm]]
