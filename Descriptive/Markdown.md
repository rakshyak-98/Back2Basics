[[Descriptive]] [[html]] [[Mermaid (DSL)]] [[LF and CRLF]]

# Markdown

> Markdown is lightweight plaintext that compiles to HTML — good for notes, READMEs, and docs-as-code.

```txt
        Markdown ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Markdown literacy is assumed

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview
- [Markdown — Wikipedia](https://en.wikipedia.org/wiki/Markdown) — overview

## Key Concepts
```txt
.md → parser (flavor) → HTML
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Flavor** | Dialect rules | “GFM tables vs strict CM.” |
| **Front matter** | YAML header | “Hugo/Obsidian metadata.” |
| **Wikilink** | `[[Note]]` | “Obsidian vault links.” |
| **Safe HTML** | Sanitization | “Don’t XSS user Markdown.” |

## Technical Details
```markdown
# Title
- list
`code`
[[Other note]]
```

| Knob | Why it matters |
|------|----------------|
| Flavor | Tables/task lists portability |
| Sanitize | User-generated MD |
| Line endings | [[LF and CRLF]] |

## Mistakes to Avoid
> [!WARNING]
> **Indentation in lists/code** — 4 spaces vs fences confuse beginners.

> [!WARNING]
> **Mixing HTML casually** — portability and XSS risks.

| Symptom | Check | Fix |
|---------|-------|-----|
| Table broken | flavor | Enable GFM |
| Link 404 | path/wikilink | Fix target note |
| XSS in HTML | raw HTML allowed | Sanitize |
| Preview ≠ GitHub | dialect drift | Stick to GFM subset |

## Pros/Cons or Trade-offs
- **Complex page layout** — real HTML/CSS.
- **Strict legal pagination** — PDF.
