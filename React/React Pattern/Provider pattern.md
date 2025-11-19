> [!NOTE]
> - It is not intended for frequently changing application state (e.g., form inputs, todo lists, shopping carts). When the Provider's value prop changes, every consumer downstream re-renders (unless you manually optimise with memoisation, splitting contexts, etc.).
> - Dan *Abramov* (Redux creator & React core team) has repeatedly said Context is for dependency injection-style sharing of infrequent or configuration-like data, not for replacing Redux/MobX/Zustand for complex app state.

- wrap a child component in a provider that handles multiple related state values and setters.
- a common approach is to use a context as a delivery mechanism for stateful values and setters.
- this pattern can be used as single pattern throughout even a large application as the single way to distribute and organize data and functionality in your entire application.

> [!WARNING]
> Accept that changes cause broad re-renders -> Nest many Providers at the root, put frequently updating state in them → performance issues

> [!NOTE] we always have a context at the root of the application, so the default values will never be used.
### Dedicated component for context management
- creating a dedicated component for the provider. This refinement addresses the intricacies of managing multiple state aspects and illustrates a more structured and maintainable way to handle complex contexts.
### Avoiding rendering everything
> [!NOTE] all component consuming a specific context will re-render when any value inside the context changes.

> [!INFO] if we want to avoid re-rendering every context consumer unnecessarily, we need to use an external library. One such library, called `use-context-selector`, allows us to not use an entire context every time. To use this we also need to create our context with this package.

 - if you are using contexts to share common functionality throughout your application, you should be using `useContextSelector` rather than the normal `useContext` hook—unless React implements the selection logic as part of the normal `useContext`
- as methods to log in and log out in one context; you can have your application data in a second context, and you can, have data controlling the UI in a third context.
- Truth be told, redux-toolkit uses this same functionality under the hood to provide its magic, so you’re getting the same performance with either method.
