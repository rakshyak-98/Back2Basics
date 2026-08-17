[[React/React data management]] [[typescript]] [[javascript]] [[css/Animation]] [[Descriptive/WCAG (Web Content Accessibility Guidelines)]]

# Intrinsic attributes (React / JSX)

> The TypeScript type for props every DOM element accepts in JSX — `className`, `onClick`, `aria-*` — **React typings + accessibility audits**.

```txt
        Intrinsic attribut ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Intrinsic sizing reviews cover width/height hints to reduce CLS in respons…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** In React + TypeScript, **`IntrinsicElements`** maps HTML tag names to their a…

```
JSX:  <button className="x" onClick={fn} />
              │
              ▼
TypeScript: React.ButtonHTMLAttributes<HTMLButtonElement>
              │
              └── enforces valid DOM props at compile time
```

| Type | Scope |
|------|-------|
| `JSX.IntrinsicElements` | All built-in tags (`div`, `input`, …) |
| `React.IntrinsicAttributes` | Universal JSX attrs (`key`, `ref`) |
| Component `Props` | Your custom interface + optional `children` |

- **Note:** Custom components do **not** automatically accept every DOM attribute unless …

## Technical Details
### Extend native element props on a wrapper

```tsx
type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'ghost';
};

function Button({ variant = 'primary', className, ...rest }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} ${className ?? ''}`}
      {...rest}   // forwards onClick, disabled, aria-*, etc.
    />
  );
}
```

### Polymorphic "as" component (keeps intrinsic attrs)

```tsx
type BoxProps<T extends React.ElementType> = {
  as?: T;
} & React.ComponentPropsWithoutRef<T>;

function Box<T extends React.ElementType = 'div'>({ as, ...props }: BoxProps<T>) {
  const Component = as ?? 'div';
  return <Component {...props} />;
}

// <Box as="a" href="/home" /> — href type-checked
```

### Common lint rule

```json
// eslint react/jsx-props-no-spreading — often disabled for design-system primitives
```

## Mistakes to Avoid
> [!WARNING]
> Spreading unknown props onto DOM nodes can inject invalid attributes silently in JS — TypeScript catches this only if your props interface is tight.

- **Mistake:** **`key` and `ref` are not props**
- **Mistake:** **Event types differ:** `onChange` on `<input>` versus custom co…
- **Mistake:** **SVG versus HTML:** separate intrinsic element maps
- **Mistake:** **React 19:** reference as prop reduces `forwardRef` boilerplate

| Symptom | Check | Fix |
|---------|-------|-----|
| TS error: Property `foo` does not exist on type `IntrinsicAttributes` | Prop passed to custom component not declared | Add to component `Props` or spread to DOM child |
| `className` vs `class` error | Using HTML attr name in JSX | Use `className` (React convention) |
| Ref not attached | Functional component without `forwardRef` | Wrap with `React.forwardRef` |
| Accessibility attrs rejected | Wrong element type | Match ARIA role to element (`button` vs `div role="button"`) |
| Spread hides invalid props | `{...props}` too permissive | Narrow with `Pick` or explicit allowlist |

## Pros/Cons or Trade-offs
- Plain JavaScript React project without TS
- Non-React frameworks (Vue `defineProps`, Svelte) — different attribute model.
