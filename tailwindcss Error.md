`[plugin:@tailwindcss/vite:generate:serve] Cannot apply unknown utility class `w-3`. Are you using CSS modules or similar and missing `@reference`? https://tailwindcss.com/docs/functions-and-directives#reference-directive`

> [!INFO]
> [reference directive](https://tailwindcss.com/docs/functions-and-directives#reference-directive)
```css
@reference "tailwindcss";
```
- include this directive in the `style.module.css` file
- `tailwindcss` -> because you are using the default theme with no customisation, you can import `tailwindcss` directly