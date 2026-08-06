[[NodeJS]]

# async utils

> One-line: what / why for **async utils** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```js
// Middleware (no more try/catch per route)
const asyncHandler = (fn) => (req, res, next) =>
	Promise.resolve(fn(req, ers, next)).catch(next);
```
```js
router.post(
	'/api',
	asyncHandler(async (req, res) => {
		const data = schema.zodValidation.parse(req.body); // throws ZodError
		const hotel = await createHotel(data, req.user?.id); // pass user for audit
		res.status(201).json({
			message: "Hotel created successfully",
			data: {id: hotel.id, name: hotel.name} // never return full object
		})
	})
)
```

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
