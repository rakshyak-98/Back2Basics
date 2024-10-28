- wrap a child component in a provider that handles multiple related state values and setters.
- a common approach is to use a context as a delivery mechanism for stateful values and setters.

> [!NOTE] we always have a context at the root of the application, so the default values will never be used.
### Dedicated component for context management
- creating a dedicated component for the provider. This refinement addresses the intricacies of managing multiple state aspects and illustrates a more structured and maintainable way to handle complex contexts.
- as methods to log in and log out in one context; you can have your application data in a second context, and you can, have data controlling the UI in a third context.