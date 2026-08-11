[[Rendering performance]]

# critical rendering path

> critical rendering path — a crucial sequence of steps that web browsers follow to convert HTML, CSS and JavaScript into a visual representation on the screen.

---

## Mental model

**Say it in one breath:** critical rendering path — plain job, how I run it, how I know it’s broken.


- is a crucial sequence of steps that web browsers follow to convert HTML, CSS and JavaScript into a visual representation on the screen.
### Pipeline
1. Document Object Model Construction
	1. the browser receives the HTML document and begins parsing it to create the DOM, a tree structure that represents the document's content and structure.
	2. this process involves converting bytes to characters, identifying tokens, and building nodes incrementally as HTML is received.
2. CSS Object Model (CSSOM) Construction
	1. after constructing the DOM, the browser processes CSS files to create the CSSOM.
	2. this model represents the styles associated with the element with the element in the DOM, allowing the browser to understand how to style the content.
3. Render Tree Creation
	1. browser combines the DOM and CSSDOM to create the Render Tree. This tree includes only the nodes that need to be rendered on the screen, omitting any elements that are not visible (like those with `display: none`) and applying styles from the CSSOM.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **critical rendering path** | Core idea of this note | “I can explain critical rendering path without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[Rendering performance]]
