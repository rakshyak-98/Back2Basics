- Redux compose -> combines multiple function from right to left into a single function.

> [!INFO]
> Apply multiple store enhancers (like `applyMiddleware`, `devtools` etc.) together.

```js
const store = createStore(rootReducer, compose(applyMiddleware(thunk), window.__REDUX_DEVTOOL__EXTENSION__?.()));
```
