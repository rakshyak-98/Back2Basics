
> [!INFO] if an event listener is added without a reference, it cannot be removed using `removeEventListener()`.
> - the reason is that `removeEventListener()` requires the exact function reference, which is missing in anonymous functions.