[[javascript]] [[Packages]]

# markup.js

> Markup.js — tiny `Mark.up(template, context)` string templates (`{{path}}`, loops, filters); not React/HTML parsing.

---

## How it works

```txt
template + context ──Mark.up──► string
```

| Feature | Example |
|---------|---------|
| Paths | `{{name.first}}` |
| Arrays | `{{list}}…{{.}}…{{/list}}` |
| Filters | `{{num\|call>toPrecision>5}}` |

---


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty output | Typo in path | Log context; fix `{{a.b}}` |
| `[object Object]` | Printed object | Pick field / custom filter |
| XSS in HTML | Untrusted context | Escape; don’t pipe raw HTML |
| `Mark is not defined` | Script not loaded | Fix script order |

---


## Gotchas

> [!WARNING]
> **Not a framework** — no reactivity; re-render manually.

> [!WARNING]
> **XSS** — treat like any HTML template; sanitize user data.

> [!WARNING]
> **Name collision** — `Mark` global; bundlers prefer ESM alternatives today.

---


## When not to use

- **React/Vue/Svelte apps** — use the framework.
- **Trusted server HTML at scale** — Handlebars/Liquid/etc. with escaping defaults.
- **Complex logic in templates** — keep logic in JS.

---


## Related

[[Packages]] [[Immer]] [[html]]

## Sources

- [Wikipedia — markup.js](https://en.wikipedia.org/wiki/markup.js)
