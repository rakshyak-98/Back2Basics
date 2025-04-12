## Two way sync strategy

localstorage -> slice
	- on app init, manual `dispatch(setx(...))`
	
slice -> localstorage
	- on state change, via `middleware` or `listenerMiddleware`

### Read from localStorage on App load
```js
const savedAuth = localStorage.getItem('auth')
const preloadedState = saveAuth ? { auth: JSON.parse(savedAuth)} : undefined;

export const store = configureStore({
	reducer: { auth: authReducer },
	preloadedState,
})

```

[initializing state](https://redux.js.org/usage/structuring-reducers/initializing-state)
there are two main ways to initialize state from you application.
- `createStore` method on accept an options `preloadedState` value as its second argument.

> [!INFO] Reducers can also specify an initial value by looking for an incoming state argument that is `undefined`, and returning the value they'
