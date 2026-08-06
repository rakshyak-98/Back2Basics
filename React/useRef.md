[[React]]

# useRef

> One-line: what / why for **useRef** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#How to forward ref to other component]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

…

## Standard config / commands

…

## How to forward ref to other component

```jsx
// ✅ WITH forwardRef - ref reaches input
const InputWrapper = React.forwardRef((props, ref) => (
  <div>
    <label>{props.label}</label>
    <input ref={ref} {...props} />  {/* ref forwarded to input */}
  </div>
));

// Parent works perfectly
function Parent() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();  // ✅ Works!
    inputRef.current?.select();
  };

  return (
    <div>
      <InputWrapper ref={inputRef} label="Name" />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
