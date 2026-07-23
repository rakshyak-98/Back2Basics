[[Descriptive]] [[React]] [[css]]

# WYSIWYG (What You See Is What You Get)

> Rich-text editing where formatted output matches published appearance — architecture is document model + toolbar + sanitizer; XSS and paste garbage are the production failures.

## Mental model

WYSIWYG editors maintain an internal **document model** (HTML DOM, ProseMirror JSON, Slate tree) synced to a visible **editable surface**. Toolbar commands mutate that model; export/publish serializes to HTML/Markdown/PDF.

```
Toolbar / shortcuts
       │
       ▼
Command layer (bold, link, heading)
       │
       ▼
Document model ◄──► contenteditable / canvas view
       │
       ▼
Serializer ──► stored HTML / JSON ──► rendered page (should match)
```

Categories:
- **contenteditable + execCommand** (legacy — avoid new builds).
- **Framework editors** — TipTap (ProseMirror), Slate, Quill, CKEditor 5, TinyMCE.
- **Block builders** — Notion-like; still WYSIWYG at block level.

## Standard config / commands

### TipTap (React) minimal

```bash
npm install @tiptap/react @tiptap/starter-kit
```

```jsx
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';

function Editor({ onChange }) {
  const editor = useEditor({
    extensions: [StarterKit],
    content: '<p>Hello</p>',
    onUpdate: ({ editor }) => onChange(editor.getHTML()),
  });
  return (
    <>
      <button onClick={() => editor.chain().focus().toggleBold().run()}>Bold</button>
      <EditorContent editor={editor} />
    </>
  );
}
```

### Sanitize on save and on render

```js
import DOMPurify from 'dompurify';

const clean = DOMPurify.sanitize(dirtyHtml, {
  ALLOWED_TAGS: ['p', 'b', 'i', 'em', 'strong', 'a', 'ul', 'ol', 'li', 'h2', 'h3'],
  ALLOWED_ATTR: ['href', 'target', 'rel'],
});
```

```html
<!-- Force rel on links added server-side -->
<a href="..." rel="noopener noreferrer">
```

### Paste handling

```js
// ProseMirror/TipTap: configure paste rules; strip Word CSS
// Quill: clipboard matchers
```

### Storage format choice

| Format | Pros | Cons |
|--------|------|------|
| HTML | Universal render | Messy; needs sanitizer |
| JSON (PM/Slate) | Structured, diffable | Custom renderer required |
| Markdown | Portable | Loses complex layout |

### CSS parity (true WYSIWYG)

```css
/* Editor stylesheet mirrors published .article-body typography */
.ProseMirror {
  font-family: var(--article-font);
  line-height: 1.6;
}
.article-body { /* same rules */ }
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Published page ≠ editor | Different CSS | Share typography stylesheet; preview route |
| XSS alert / script execution | Raw `{@html}` / `dangerouslySetInnerHTML` | DOMPurify; CSP `script-src` |
| Paste from Word breaks layout | Inline styles in paste | Strip styles on paste; `pasteRules` |
| Empty paragraphs / br spam | contenteditable quirks | Use mature editor; normalize on export |
| Undo broken across transactions | Custom commands bypass history | Use editor's chain API |
| Mobile keyboard covers toolbar | Fixed toolbar z-index | `visualViewport` adjust; bottom sheet UI |
| Huge HTML in DB | Nested spans from toggles | Normalize schema; store JSON |

## Gotchas

> [!WARNING]
> **Never trust stored HTML** — sanitize on write **and** read; CSP as backstop ([[Security]] / content security policy).

> [!WARNING]
> **`contenteditable` alone** — cross-browser inconsistency; you'll rebuild TipTap poorly.

> [!WARNING]
> **Markdown WYSIWYG hybrids** — round-trip loses formatting; pick canonical format.

> [!WARNING]
> **Collaboration** — CRDT/OT (Yjs) is separate concern from WYSIWYG shell.

## When NOT to use

- **Developer-only content (Markdown in git)** — plain MD + preview is simpler.
- **Highly structured content (products, legal clauses)** — use structured CMS fields, not free-form HTML.
- **Email composition** — email HTML is its own nightmare; use email-specific builders.

## Related

[[React]] [[css]] [[Security]] [[Descriptive]]
