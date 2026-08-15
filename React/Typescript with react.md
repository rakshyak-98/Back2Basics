[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# TypeScript with React

> Type props, hooks, and events so invalid JSX and wrong hook values fail at compile time.

## Interview Relevance

Interviewers check `PropsWithChildren`, event types, generics on hooks, and how you type context without `any`.

## Sources

- [React — TypeScript](https://react.dev/learn/typescript) — deep-dive
- [TS Handbook — JSX](https://www.typescriptlang.org/docs/handbook/jsx.html) — overview

## Core Definition

TypeScript models the component contract: props in, events out, and hook return shapes — React runtime stays the same.

## Key Concepts

- **Props interfaces:** explicit required vs optional fields.
- **Children:** `React.PropsWithChildren` or `children?: React.ReactNode`.
- **Events:** `React.ChangeEvent<HTMLInputElement>`, not `any`.
- **Generics:** `useState<User | null>(null)` for discriminated loading states.

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

## Real-World Applications

Shared `User` type imported by API client, query hooks, and form components — one change updates all call sites.

## Pros/Cons or Trade-offs

- **Pro:** Refactors and illegal props caught before QA.
- **Con:** Over-narrow unions fight real backend variance.

## Comparison

- vs PropTypes: TypeScript erases at compile time; PropTypes were runtime checks.

## Mistakes to Avoid

- `children: any` / `as any` to silence errors.
- Typing JSX results as `Element` when `ReactNode` is needed.
