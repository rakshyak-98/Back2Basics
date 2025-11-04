
> [!INFO] if an event listener is added without a reference, it cannot be removed using `removeEventListener()`.
> - the reason is that `removeEventListener()` requires the exact function reference, which is missing in anonymous functions.

**Internal behavior**
- Event system stores listeners in array-like list per event type
- On event dispatch: it iterates the list in registration order
- No guarantee about async timing, but order is deterministic
- `stopPropagation()` stops bubbling to other elements, not sibling listeners on same element
- Removing: `removeEventListener` requires same function reference.

> [!WARNING]
> If a listener calls `stopImmediatePropagation()`, no further listeners on the same element will run

> [!INFO]
> For multiple `click` listeners on the same element, JavaScript does not overwrite previous ones.
> They are pushed into an internal *event listener list* and executed in the order they were registered (FIFO).