[[Descriptive]] [[html]] [[Mermaid (DSL)]]

# Markdown

> Markdown is lightweight plaintext that compiles to HTML — good for notes, READMEs, and docs-as-code.

---

## How it works

```txt
.md → parser (flavor) → HTML
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Flavor** | Dialect rules | “GFM tables vs strict CM.” |
| **Front matter** | YAML header | “Hugo/Obsidian metadata.” |
| **Wikilink** | `[[Note]]` | “Obsidian vault links.” |
| **Safe HTML** | Sanitization | “Don’t XSS user Markdown.” |

---


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Table broken | flavor | Enable GFM |
| Link 404 | path/wikilink | Fix target note |
| XSS in HTML | raw HTML allowed | Sanitize |
| Preview ≠ GitHub | dialect drift | Stick to GFM subset |

---


## Gotchas

> [!WARNING]
> **Indentation in lists/code** — 4 spaces vs fences confuse beginners.

> [!WARNING]
> **Mixing HTML casually** — portability and XSS risks.

---


## When not to use

- **Complex page layout** — real HTML/CSS.
- **Strict legal pagination** — PDF.


## Related

[[html]] [[LF and CRLF]] [[Mermaid (DSL)]]

## Sources

- [Wikipedia — Markdown](https://en.wikipedia.org/wiki/Markdown)
