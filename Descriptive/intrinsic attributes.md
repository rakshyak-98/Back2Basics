[[React/React data management]] [[typescript]] [[javascript]] [[css/Animation]]

# Intrinsic attributes (React / JSX)

> The TypeScript type for props every DOM element accepts in JSX — `className`, `onClick`, `aria-*` — **React typings + accessibility audits**.

## Mental model

In React + TypeScript, **`IntrinsicElements`** maps HTML tag names to their allowed attributes. **`IntrinsicAttributes`** is the small set every JSX element gets (mainly `key` and `ref`). Component authors extend this when wrapping native elements.

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

Custom components do **not** automatically accept every DOM attribute unless you forward them (spread or explicit passthrough).

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| TS error: Property `foo` does not exist on type `IntrinsicAttributes` | Prop passed to custom component not declared | Add to component `Props` or spread to DOM child |
| `className` vs `class` error | Using HTML attr name in JSX | Use `className` (React convention) |
| Ref not attached | Functional component without `forwardRef` | Wrap with `React.forwardRef` |
| Accessibility attrs rejected | Wrong element type | Match ARIA role to element (`button` vs `div role="button"`) |
| Spread hides invalid props | `{...props}` too permissive | Narrow with `Pick` or explicit allowlist |

## Gotchas

> [!WARNING]
> Spreading unknown props onto DOM nodes can inject invalid attributes silently in JS — TypeScript catches this only if your props interface is tight.

- **`key` and `ref` are not props** — they live on `IntrinsicAttributes`, not in `props` inside the component.
- **Event types differ:** `onChange` on `<input>` vs custom component needs explicit typing.
- **SVG vs HTML:** separate intrinsic element maps — `<svg>` attrs differ from `<div>`.
- **React 19:** ref as prop reduces `forwardRef` boilerplate — check your React version typings.

## When NOT to use

- Plain JavaScript React project without TS — compiler won't enforce intrinsic attrs.
- Non-React frameworks (Vue `defineProps`, Svelte) — different attribute model.

## Related

[[React/React data management]] [[Descriptive/WCAG (Web Content Accessibility Guidelines)]] [[typescript]] [[javascript]]
