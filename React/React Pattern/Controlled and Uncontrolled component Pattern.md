[[React Pattern]] [[useRef]] [[react hooks]]

# Controlled and Uncontrolled component Pattern

> Controlled: React state is the source of truth for the input. Uncontrolled: the DOM holds the value; you read it via ref when needed.

---

## Mental model

**Say it in one breath:** Controlled = `value` + `onChange` every keystroke. Uncontrolled = `defaultValue` + ref/`FormData` on submit.

```txt
Controlled:   state ──value──► <input> ──onChange──► setState
Uncontrolled: defaultValue ► <input> … later ref.current.value
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Controlled** | React owns the value | “Validate and disable as they type.” |
| **Uncontrolled** | DOM owns the value | “Simple forms; less re-render.” |
| **defaultValue** | Initial only | “Changing it later won’t update the input.” |

## Standard config / commands

```tsx
// Controlled
const [name, setName] = useState('')
<input value={name} onChange={(e) => setName(e.target.value)} />

// Uncontrolled
const ref = useRef<HTMLInputElement>(null)
<input defaultValue="Ada" ref={ref} />
// submit: ref.current?.value
```

| Use when | Pattern |
|----------|---------|
| Live validation / dependent fields | Controlled |
| File inputs / little React involvement | Uncontrolled |
| Design system form libs | Often controlled under the hood |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Input won’t type | `value` set, no `onChange` | Add handler or drop `value` |
| Cursor jumps | Recreating value oddly | Keep string state; don’t reset each render |
| `defaultValue` ignored later | Expected controlled updates | Switch to `value` |
| Switching modes mid-life | Warned by React | Pick one; remount with `key` |

---

## Gotchas

> [!WARNING]
> **Don’t mix `value` and `defaultValue`** — React warns; pick a mode.

> [!WARNING]
> **File inputs are uncontrolled** — you cannot set `value` for security reasons.

---

## When NOT to use

- **Fully controlled everything in a 40-field form** — consider form libs + uncontrolled fields where fine.
- **Uncontrolled when parent must sync** — need controlled.

---

## Related

[[useRef]] [[React Pattern/Component Presentational Pattern]]
