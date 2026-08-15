[[javascript]] [[Packages]] [[Immer]] [[html]]

# markup.js

> Markup.js — tiny `Mark.up(template, context)` string templates (`{{path}}`, loops, filters); not React/HTML parsing.

## Interview Relevance

Interviewers probe **markup.js** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Wikipedia — markup.js](https://en.wikipedia.org/wiki/markup.js) — overview

## Key Concepts

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

## Real-World Applications

In production APIs and tooling, **markup.js** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Not a framework** — no reactivity; re-render manually; **XSS** — treat like any HTML template; sanitize user data.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Markup.js — tiny `Mark.up(template, context)` string templates (`{{path}}`, loop…).
- **Con / when not:** **React/Vue/Svelte apps** — use the framework.
- **Con / when not:** **Trusted server HTML at scale** — Handlebars/Liquid/etc. with escaping defaults.
- **Con / when not:** **Complex logic in templates** — keep logic in JS.

## Comparison

vs [[Packages]]: know when each applies — do not treat them as interchangeable. vs [[Immer]]: know when each applies — do not treat them as interchangeable. vs [[html]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Not a framework** — no reactivity; re-render manually.
- **XSS** — treat like any HTML template; sanitize user data.
- **Name collision** — `Mark` global; bundlers prefer ESM alternatives today.
- **Empty output:** check Typo in path; fix: Log context; fix `{{a.b}}`
- **`[object Object]`:** check Printed object; fix: Pick field / custom filter
- **XSS in HTML:** check Untrusted context; fix: Escape; don’t pipe raw HTML
- **`Mark is not defined`:** check Script not loaded; fix: Fix script order
