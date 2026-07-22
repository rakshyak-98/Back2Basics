[[Descriptive/web development]] [[css/Animation]] [[React/React data management]] [[Security/content security policy]]

# WCAG (Web Content Accessibility Guidelines)

> W3C recommendations for perceivable, operable, understandable, robust web content — legal and UX baseline — **WCAG 2.2 + WAI**.

## Mental model

WCAG defines **success criteria** grouped under four principles (**POUR**):

```
Perceivable   → alt text, contrast, captions
Operable      → keyboard, no seizure triggers, enough time
Understandable→ readable, predictable, input help
Robust        → valid markup, assistive tech compatible
```

Conformance **levels**: **A** (minimum), **AA** (industry standard / many laws), **AAA** (aspirational, not always feasible site-wide).

Developed by W3C **WAI** (Web Accessibility Initiative) — referenced by ADA, EN 301 549, Section 508.

## Standard config / commands

### Level summary (what teams actually ship)

| Level | Examples |
|-------|----------|
| **A** | Alt text for images; form labels; no keyboard traps |
| **AA** | Contrast ≥ 4.5:1 body text; resize 200%; focus visible; skip links |
| **AAA** | Contrast 7:1; sign language for all video — rare full-site |

### Quick HTML patterns

```html
<img src="chart.png" alt="Q3 revenue up 12% year over year">

<label for="email">Email</label>
<input id="email" type="email" autocomplete="email" required>

<button type="button" aria-expanded="false" aria-controls="menu">
  Menu
</button>

<a href="#main" class="skip-link">Skip to content</a>
```

### Focus management (React modal)

```javascript
useEffect(() => {
  if (!open) return;
  const prev = document.activeElement;
  dialogRef.current?.focus();
  return () => (prev instanceof HTMLElement && prev.focus());
}, [open]);
```

### Automated checks (CI gate — catches ~30–50% of issues)

```bash
npm i -D @axe-core/cli
npx axe https://localhost:3000 --exit
# Also: Lighthouse accessibility audit, eslint-plugin-jsx-a11y
```

### Color contrast check

- Foreground `#595959` on white → verify with WebAIM contrast checker
- Don't rely on color alone for errors — add icon + text

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Audit fails contrast | Brand colors | Adjust palette or use AA exceptions (large text 3:1) |
| Keyboard can't reach control | `tabindex`, CSS `display:none` on focusable | Native `<button>`; visible `:focus-visible` |
| Screen reader silent on update | No live region | `aria-live="polite"` on status toast |
| Form errors not announced | Error only red border | Link `aria-describedby` to error text |
| Custom widget wrong role | Div soup | Use semantic HTML first; ARIA only when needed |

## Gotchas

> [!WARNING]
> **Accessibility overlays** (widget that "fixes" your site) do not transfer liability and often break AT — fix source HTML/CSS/JS.

- **`aria-label` on wrong element** hides visible text from AT if misapplied.
- **Auto-playing video** fails 2.2.x criteria unless user control within seconds.
- **PDF-only** content fails unless tagged accessible PDF — HTML preferred.
- **AA is the contract** — claiming AAA on one page ≠ whole product AAA.

## When NOT to use

- WCAG is not a substitute for **user testing** with assistive technology users.
- Don't block ship on AAA contrast for decorative hero imagery — mark decorative `alt=""`.

## Related

[[Descriptive/web development]] [[css/Animation]] [[React/React data management]] [[Security/content security policy]]
