[[flutter]] [[dart/dart functions]] [[Design pattern/Observer]]

# Flutter widget

> Immutable UI description nodes — Flutter rebuilds widgets; `State` and `Element` hold what survives across frames.





## Interview Relevance
Interviewers probe `StatelessWidget` vs `StatefulWidget`, why `builder` delays construction, and that `BuildContext` is a handle into the element tree — not “the widget itself.”

## Sources
- [Flutter — Introduction to widgets](https://docs.flutter.dev/ui/widgets-intro) — overview
- [Flutter — Navigation and routing](https://docs.flutter.dev/ui/navigation) — deep-dive

## Key Concepts
- **Widget:** configuration object (cheap, immutable) → describe UI; do not hold long-lived mutable UI state here.
- **Element / RenderObject:** framework bookkeeping and layout/paint → where identity and constraints live.
- **`BuildContext`:** location in the tree → `Theme.of(context)`, `Navigator`, inherited widgets.
- **Route `builder`:** recipe executed when the route is pushed → avoids building the next screen early; supplies the new route’s context.
- **Keys:** preserve element identity across rebuilds → lists, forms, `GlobalKey` for rare cross-tree access.

## Technical Details
`MaterialPageRoute` takes a builder, not a pre-built widget instance:

```dart
Navigator.of(context).push(
  MaterialPageRoute(
    builder: (BuildContext context) => MyNewScreen(id: itemId),
  ),
);
```

Why builder matters:

- Defers construction until navigation happens (recipe vs baked cake).
- Gives a `BuildContext` for the *new* route, not the screen you left.
- Lets you pass arguments computed at push time.

| Type | Holds mutable UI state? | Typical use |
|------|-------------------------|-------------|
| `StatelessWidget` | No | Pure layout from props |
| `StatefulWidget` + `State` | Yes (`State`) | Controllers, animation, form fields |

## Real-World Applications
Feature screens: push with builder + args; read theme/media via context; keep business state in a state-management layer above leaf widgets.

**Example:** Prefetching a heavy screen widget before push wastes memory — pass ids into the builder and load inside `initState` / a provider.

## Pros/Cons or Trade-offs
- **Pro:** Declarative rebuilds make UI predictable when state is explicit.
- **Con:** Overusing `setState` high in the tree rebuilds too much — split widgets or use selective listeners.

## Comparison
- vs React components: similar props→UI idea; Flutter separates Widget / Element / RenderObject more explicitly.
- vs imperative Android Views: you mutate a view hierarchy; Flutter rebuilds widget descriptions.

## Mistakes to Avoid
- Storing app state only in widgets that get disposed on navigation.
- Using the *old* screen’s context after an async gap post-`push`/`pop` without checking `mounted`.
- Passing a constructed widget into APIs that expect a `builder` and wondering why context/`InheritedWidget` lookups fail.
