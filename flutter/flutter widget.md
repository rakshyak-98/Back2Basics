[[flutter]] [[dart/dart functions]] [[Design pattern/Observer]]

# Flutter widget

> Immutable UI description nodes — Flutter rebuilds widgets; `State` and `Element` hold what survives across frames.

```txt
        Flutter widget ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe `StatelessWidget` vs `StatefulWidget`, why `builder` delay…

## Sources
- [Flutter — Introduction to widgets](https://docs.flutter.dev/ui/widgets-intro) — overview
- [Flutter — Navigation and routing](https://docs.flutter.dev/ui/navigation) — deep-dive

## Key Concepts
- **Widget:** configuration object (cheap, immutable) → describe UI
- **Element / RenderObject:** framework bookkeeping and layout/paint → where identity and constraints live.
- **`BuildContext`:** location in the tree → `Theme.of(context)`, `Navigator`, inherited widgets.
- **Route `builder`:** recipe executed when the route is pushed → avoids building the next screen ea…
- **Keys:** preserve element identity across rebuilds → lists, forms, `GlobalKey` for rar…

## Technical Details
- `MaterialPageRoute` takes a builder, not a pre-built widget instance:

```dart
Navigator.of(context).push(
  MaterialPageRoute(
    builder: (BuildContext context) => MyNewScreen(id: itemId),
  ),
);
```

- Why builder matters:

- Defers construction until navigation happens (recipe vs baked cake).
- Gives a `BuildContext` for the *new* route, not the screen you left.
- Lets you pass arguments computed at push time.

| Type | Holds mutable UI state? | Typical use |
|------|-------------------------|-------------|
| `StatelessWidget` | No | Pure layout from props |
| `StatefulWidget` + `State` | Yes (`State`) | Controllers, animation, form fields |

## Mistakes to Avoid
- **Mistake:** Storing app state only in widgets that get disposed on navigation
- **Mistake:** Using the *old* screen’s context after an async gap post-`push`/…
- **Mistake:** Passing a constructed widget into APIs that expect a `builder` a…

## Pros/Cons or Trade-offs
- **Pro:** Declarative rebuilds make UI predictable when state is explicit.
- **Con:** Overusing `setState` high in the tree rebuilds too much — split widgets or use selective listeners.

## Comparison
- vs React components: similar props→UI idea
- vs imperative Android Views: you mutate a view hierarchy; Flutter rebuilds widget descriptions.


### Use cases
- Feature screens: push with builder + args

- **Example:** Prefetching a heavy screen widget before push wastes memory
