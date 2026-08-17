[[react hooks]] [[React State management]] [[React Architecture]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]] [[Data Fetching HOC component]]

# Managing complex component structure

> Keep large UIs navigable — feature folders, composition, and clear ownership instead of one 2k-line component.





## Interview Relevance
Interviewers ask how you structure features, shared UI, and cross-cutting providers in a growing React app.

## Sources
- [Thinking in React](https://react.dev/learn/thinking-in-react) — overview
- [Managing State](https://react.dev/learn/managing-state) — deep-dive

## Core Definition
Complex UI stays maintainable when components are composed in a hierarchy with clear state owners and feature boundaries.

## Key Concepts
- **Feature folders:** UI + hooks + API colocated.
- **Lift state sparingly:** only as high as shared need.
- **Compound / context:** for interrelated subcomponents ([[React Pattern/Compound Components]]).

## Technical Details
Suggested layout:

```txt
features/checkout/
  CheckoutPage.tsx
  useCheckout.ts
  components/
  api.ts
shared/ui/
```

## Real-World Applications
Checkout grew to payment + address + review — split into compound steps with one checkout hook owning the draft.

## Pros/Cons or Trade-offs
- **Pro:** Parallel team work on features.
- **Con:** Over-nesting folders for tiny widgets.

## Comparison
- vs [[React Architecture]]: architecture is the system view; this is the component-tree craft.

## Mistakes to Avoid
- God component with all modals and tabs.
- Context that wraps the entire app for one rarely used value.
