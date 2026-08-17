[[react hooks]] [[React State management]] [[React Architecture]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]] [[Data Fetching HOC component]]

# Managing complex component structure

> Keep large UIs navigable — feature folders, composition, and clear ownership instead of one 2k-line component.

```txt
        Managing complex c ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask how you structure features, shared UI, and cross-cutting pro…

## Sources
- [Thinking in React](https://react.dev/learn/thinking-in-react) — overview
- [Managing State](https://react.dev/learn/managing-state) — deep-dive

## Key Concepts
- **Feature folders:** UI + hooks + API colocated.
- **Lift state sparingly:** only as high as shared need.
- **Compound / context:** for interrelated subcomponents ([[React Pattern/Compound Components]]).


- **Core:** Complex UI stays maintainable when components are composed in a hierarchy wit…

## Technical Details
- Suggested layout:

```txt
features/checkout/
  CheckoutPage.tsx
  useCheckout.ts
  components/
  api.ts
shared/ui/
```

## Mistakes to Avoid
- **Mistake:** God component with all modals and tabs
- **Mistake:** Context that wraps the entire app for one rarely used value

## Pros/Cons or Trade-offs
- **Pro:** Parallel team work on features.
- **Con:** Over-nesting folders for tiny widgets.

## Comparison
- vs [[React Architecture]]: architecture is the system view; this is the component-tree craft.


### Use cases
- Checkout grew to payment + address + review
