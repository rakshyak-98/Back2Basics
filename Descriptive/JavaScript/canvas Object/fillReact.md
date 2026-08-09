[[Javascript]] [[html]]

# fillReact

> `fillRect` paints a filled axis-aligned rectangle on a canvas 2D context (note: often mistyped as fillReact).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Set `fillStyle`, then `fillRect(x, y, w, h)` in canvas pixel space — not DOM React.

```txt
getContext('2d') → fillStyle → fillRect
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Canvas** | Immediate bitmap API | “No retained rect nodes.” |
| **fill vs stroke** | Interior vs outline | `fillRect` / `strokeRect` |
| **Origin** | Top-left of canvas | “y grows downward.” |
| **DPR** | Device pixel ratio | “Scale for sharp retina.” |

---

## Standard config / commands

```js
const ctx = canvas.getContext('2d')
ctx.fillStyle = '#3366ff'
ctx.fillRect(10, 20, 100, 50)
```

| Knob | Why it matters |
|------|----------------|
| `fillStyle` | Color/pattern before draw |
| Canvas width attrs | CSS size ≠ bitmap size |
| clearRect | Erase before redraw |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Nothing draws | context / size 0 | Set width/height attrs |
| Blurry | DPR mismatch | Scale canvas by `devicePixelRatio` |
| Wrong color | style after draw | Set style first |
| fillReact undefined | typo | Use `fillRect` |

---

## Gotchas

> [!WARNING]
> **CSS scales the bitmap** — setting only CSS width blurs; set attributes too.

> [!WARNING]
> **Name mix-up with React** — canvas API is unrelated to React.

---

## When NOT to use

- **Simple UI boxes** — HTML/CSS.
- **Huge scene graphs** — WebGL / retained mode libs.

## Related

[[html]] [[Javascript]]
