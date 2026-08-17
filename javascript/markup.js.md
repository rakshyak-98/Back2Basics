[[javascript]] [[Packages]] [[Immer]] [[html]]

# markup.js

> Markup.js — tiny `Mark.up(template, context)` string templates (`{{path}}`, loops, filters); not React/HTML parsing.

```txt
        markup.js ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **markup.js** to see if you understand what it does operat…

## Sources
- [Wikipedia — markup.js](https://en.wikipedia.org/wiki/markup.js) — overview

## Technical Details
```txt
template + context ──Mark.up──► string
```

| Feature | Example |
|---------|---------|
| Paths | `{{name.first}}` |
| Arrays | `{{list}}…{{.}}…{{/list}}` |
| Filters | `{{num\|call>toPrecision>5}}` |

```html
<script src="markup.min.js"></script>
```

```js
Mark.up('Hi, {{name.first}}!', { name: { first: 'Ada' } })

Mark.up('<ul>{{bros}}<li>{{.}}</li>{{/bros}}</ul>', {
  bros: ['Jack', 'Joe'],
})
```

| Knob | Why it matters |
|------|----------------|
| Context shape | Missing paths → empty |
| Filters | Pipe transforms |
| Escape | Know if output is trusted |

## Mistakes to Avoid
- **Mistake:** **Not a framework** — no reactivity; re-render manually
- **Mistake:** **XSS** — treat like any HTML template; sanitize user data
- **Mistake:** **Name collision**
- **Mistake:** **Empty output:** check Typo in path
- **Mistake:** **`[object Object]`:** check Printed object
- **Mistake:** **XSS in HTML:** check Untrusted context
- **Mistake:** **`Mark is not defined`:** check Script not loaded

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Markup.js — tiny `Mark.up(template, context)` string templates (`{{path}}`, loop…).
- **Con / when not:** **React/Vue/Svelte apps** — use the framework.
- **Con / when not:** **Trusted server HTML at scale**
- **Con / when not:** **Complex logic in templates** — keep logic in JS.

## Comparison
- vs [[Packages]]: know when each applies


### Use cases
- In production APIs and tooling, **markup.js** shows up whenever teams ship No…
