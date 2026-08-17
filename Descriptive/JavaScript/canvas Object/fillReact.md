[[Javascript]] [[html]]

# fillReact

> `fillRect` paints a filled axis-aligned rectangle on a canvas 2D context (note: often mistyped as fillReact).

```txt
        fillReact ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers may probe fillReact as tooling or web platform literacy

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
getContext('2d') → fillStyle → fillRect
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Canvas** | Immediate bitmap API | “No retained rect nodes.” |
| **fill vs stroke** | Interior vs outline | `fillRect` / `strokeRect` |
| **Origin** | Top-left of canvas | “y grows downward.” |
| **DPR** | Device pixel ratio | “Scale for sharp retina.” |

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> **CSS scales the bitmap** — setting only CSS width blurs; set attributes too.

> [!WARNING]
> **Name mix-up with React** — canvas API is unrelated to React.

| Symptom | Check | Fix |
|---------|-------|-----|
| Nothing draws | context / size 0 | Set width/height attrs |
| Blurry | DPR mismatch | Scale canvas by `devicePixelRatio` |
| Wrong color | style after draw | Set style first |
| fillReact undefined | typo | Use `fillRect` |

## Pros/Cons or Trade-offs
- **Simple UI boxes** — HTML/CSS.
- **Huge scene graphs** — WebGL / retained mode libs.
