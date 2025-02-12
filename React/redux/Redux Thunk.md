You don't need explicit Thunk middleware configuration in the latest React Redux Toolkit (RTK) till (2024).
### RTK Includes Thunk by default
- `configureStore` automatically includes `redux-thunk` in its middleware setup.
- no need to manually add it unless you want custom configurations.
#### Middleware auto-setup
`getDefaultMiddleware()` already has `thunk`, `serializableChunk`, and `immutableCheck`.

> [!INFO] When you want to override the default middleware, e.g., add `logger` or disable `serializableCheck`. You need to configure `thunk`.


### What is redux thunk?
- middleware for redux that allows you to write asynchronous logic (API calls) inside action creators. Without it, [[Redux]] only handle synchronous actions.

> [!INFO] Redux actions are pure function, meaning they can't have side effects like API calls or delays. We need thunk to handle them.
- If we need to fetch data from an API, Redux alone can't handle it.