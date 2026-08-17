[[Descriptive]] [[Markdown]] [[embedded image]] [[WCAG (Web Content Accessibility Guidelines)]]

# html

> HTML is the document structure browsers parse — elements, attributes, and accessibility tree roots.

```txt
        html ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** HTML interviews check semantics, accessibility, and what belongs in markup ve…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
HTML → DOM → CSSOM → render
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Semantic tags** | Meaning | “Use `button`, not clickable `div`.” |
| **DOM** | Live tree | “JS mutates nodes.” |
| **void elements** | No close tag | `img`, `br`, `input` |
| **forms** | Submit model | “name → payload.” |

## Technical Details
```html
<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>App</title></head>
  <body>
    <main>
      <h1>Title</h1>
      <button type="button">Save</button>
    </main>
  </body>
</html>
```

| Knob | Why it matters |
|------|----------------|
| `lang` | A11y / hyphenation |
| `alt` on images | Screen readers |
| `type` on button | Avoid accidental submit |

## Mistakes to Avoid
> [!WARNING]
> **Clickable divs without keyboard** — not accessible.

> [!WARNING]
> **Inline scripts before DOM** — null querySelector; defer/DOMContentLoaded.

| Symptom | Check | Fix |
|---------|-------|-----|
| Quirks mode | missing doctype | Add `<!doctype html>` |
| Broken layout | invalid nesting | Validate HTML |
| Form weird POST | button type | `type="button"` |
| A11y fails | div soup | Semantic elements + labels |

## Pros/Cons or Trade-offs
- **Non-document UIs** — canvas/WebGL still need a host page.
- **Data interchange** — JSON, not HTML scraping.
