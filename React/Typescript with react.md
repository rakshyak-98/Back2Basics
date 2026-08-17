[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# TypeScript with React

> Type props, hooks, and events so invalid JSX and wrong hook values fail at compile time.

```txt
        TypeScript with Re ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers check `PropsWithChildren`, event types, generics on hooks, and h…

## Sources
- [React — TypeScript](https://react.dev/learn/typescript) — deep-dive
- [TS Handbook — JSX](https://www.typescriptlang.org/docs/handbook/jsx.html) — overview

## Key Concepts
- **Props interfaces:** explicit required vs optional fields.
- **Children:** `React.PropsWithChildren` or `children?: React.ReactNode`.
- **Events:** `React.ChangeEvent<HTMLInputElement>`, not `any`.
- **Generics:** `useState<User | null>(null)` for discriminated loading states.


- **Core:** TypeScript models the component contract: props in, events out, and hook retu…

## Technical Details
```tsx
type ButtonProps = {
  variant: 'primary' | 'ghost'
  onPress: () => void
  children: React.ReactNode
}
function Button({ variant, onPress, children }: ButtonProps) {
  return <button data-variant={variant} onClick={onPress}>{children}</button>
}
```

## Mistakes to Avoid
- **Mistake:** `children: any` / `as any` to silence errors
- **Mistake:** Typing JSX results as `Element` when `ReactNode` is needed

## Pros/Cons or Trade-offs
- **Pro:** Refactors and illegal props caught before QA.
- **Con:** Over-narrow unions fight real backend variance.

## Comparison
- vs PropTypes: TypeScript erases at compile time; PropTypes were runtime checks.


### Use cases
- Shared `User` type imported by API client, query hooks, and form components
