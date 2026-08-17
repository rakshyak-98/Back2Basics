[[react hooks]] [[React State management]] [[React Architecture]] [[Compound Components]] [[Compound Components 1]] [[Stack from scratch]]

# Separate functional logic from presentation components

> Split hooks/data logic from JSX-only views — test and reuse behavior without caring about markup.

```txt
        Separate functiona ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask how you separate container/logic from presentational UI and …

## Sources
- [React — Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) — deep-dive
- [Thinking in React](https://react.dev/learn/thinking-in-react) — overview

## Key Concepts
- **Logic layer:** custom hooks / containers own state and effects.
- **Presentation:** receive props, emit events, avoid fetching.
- **Boundary:** presentational components stay reusable across screens.


- **Core:** Keep data fetching, subscriptions, and business rules in hooks or thin contai…

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

## Mistakes to Avoid
- **Mistake:** Fetching inside every presentational leaf
- **Mistake:** Passing the entire store/query client as props “to keep it pure.”

## Pros/Cons or Trade-offs
- **Pro:** Easier unit tests for logic without rendering full trees.
- **Con:** Over-splitting tiny components adds file noise.

## Comparison
- vs [[React Pattern/Component Presentational Pattern]]: same idea; hooks are the modern container.


### Use cases
- Design system Button stays dumb
