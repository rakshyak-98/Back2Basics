[[react hooks]] [[React State management]] [[React Architecture]] [[Compound Components]] [[Compound Components 1]] [[Stack from scratch]]

# Separate functional logic from presentation components

> Split hooks/data logic from JSX-only views — test and reuse behavior without caring about markup.





## Interview Relevance
Interviewers ask how you separate container/logic from presentational UI and whether hooks replaced classic container components.

## Sources
- [React — Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) — deep-dive
- [Thinking in React](https://react.dev/learn/thinking-in-react) — overview

## Core Definition
Keep data fetching, subscriptions, and business rules in hooks or thin containers; leave presentational components mostly props → JSX.

## Key Concepts
- **Logic layer:** custom hooks / containers own state and effects.
- **Presentation:** receive props, emit events, avoid fetching.
- **Boundary:** presentational components stay reusable across screens.

## Technical Details
```tsx
function useUser(id: string) {
  return useQuery({ queryKey: ['user', id], queryFn: () => api.user(id) })
}
function UserCardView({ name, onEdit }: { name: string; onEdit: () => void }) {
  return <article><h2>{name}</h2><button onClick={onEdit}>Edit</button></article>
}
function UserCard({ id }: { id: string }) {
  const { data } = useUser(id)
  return <UserCardView name={data.name} onEdit={() => navigate('edit')} />
}
```

## Real-World Applications
Design system Button stays dumb; feature `CheckoutButton` hook owns cart mutation and disabled state.

## Pros/Cons or Trade-offs
- **Pro:** Easier unit tests for logic without rendering full trees.
- **Con:** Over-splitting tiny components adds file noise.

## Comparison
- vs [[React Pattern/Component Presentational Pattern]]: same idea; hooks are the modern container.

## Mistakes to Avoid
- Fetching inside every presentational leaf.
- Passing the entire store/query client as props “to keep it pure.”
