[[react hooks]] [[React State management]] [[React Architecture]] [[data fetching component]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]]

# Data Fetching HOC component

> Higher-order component that loads data and injects props — legacy pattern largely replaced by hooks and query libraries.

## Interview Relevance

Interviewers may show `withUser(Component)` and ask how you’d redo it with hooks or React Query.

## Sources

- [Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) — deep-dive
- [Legacy HOCs](https://legacy.reactjs.org/docs/higher-order-components.html) — overview

## Core Definition

A data-fetching HOC wraps a view, loads remote data, and passes results as props — composition via wrapping.

## Key Concepts

- **withX(Component):** returns enhanced component.
- **Prop collision:** injected names can clash.
- **Hooks era:** `useUser()` + [[react-query]] preferred.

## Technical Details

```tsx
function withUser(Wrapped: React.ComponentType<{ user: User }>) {
  return function WithUser(props: object) {
    const { data } = useQuery({ queryKey: ['me'], queryFn: api.me })
    if (!data) return null
    return <Wrapped {...props} user={data} />
  }
}
```

## Real-World Applications

Older codebases still wrap route pages in `withAuth` / `withData` HOCs; migrate edge-in with hooks.

## Pros/Cons or Trade-offs

- **Pro:** Reuse fetch+gate logic across class components.
- **Con:** Wrapper pyramids, opaque props, weak TypeScript.

## Comparison

- vs [[React Pattern/Higher order Component (HOCs)]]: this is the data-loading specialty of HOCs.

## Mistakes to Avoid

- Stacking HOCs until display names and props are untraceable.
- Fetching in HOC and again inside the wrapped component.
