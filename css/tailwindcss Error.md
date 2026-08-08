[[css]]

# tailwindcss Error

> tailwindcss Error — [plugin:@tailwindcss/vite:generate:serve] Cannot apply unknown utility class w-3. Are you using CSS modules or similar and missing @reference? https://tailwindcss.com/docs/functions-and-directives#reference-directive

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

`[plugin:@tailwindcss/vite:generate:serve] Cannot apply unknown utility class `w-3`. Are you using CSS modules or similar and missing `@reference`? https://tailwindcss.com/docs/functions-and-directives#reference-directive`
> [!INFO]
> [reference directive](https://tailwindcss.com/docs/functions-and-directives#reference-directive)
```css
@reference "tailwindcss";
```
- include this directive in the `style.module.css` file
- `tailwindcss` -> because you are using the default theme with no customisation, you can import `tailwindcss` directly

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
