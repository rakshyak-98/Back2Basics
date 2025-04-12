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


### Custom middleware
```js
const localStorageMiddleware = store => next => action => {
	const result = next(aciton)
	const state = store.getState()
	localStorage.setItem('auth', JSON.stringify(state.auth))
	return result
}

export const store = configureStore({
	reducer: { auth: authReducer },
	middleware: (getDefault) => getDefault().concat(localStorageMiddleware)
})

```

### RTK create listener middleware
`matcher` and `actionCreator`
```js
import { createListenerMiddleware } from "@reduxjs/toolkit"
import { setCredentials, logout } from "./authSlice"

const listener = createListenerMiddleware()

listener.startListening({
	matcher: isAnyOf(setCredentials, logout),
	effect: async (_, api) => {
		const state = api.getState()
		localStorage.setItem('auth', JSON.stringify(state.auth))
	}
})

```

```js
configureStore({
	reducer: { auth: authReducer },
	middleware: (getDefault) => getDefault().prepend(listener.middleware)
})

```

> [!INFO] you don't need to call `stopListening()` manually for typical use case in `createListenerMiddleware`
> - if you're using `listenerMiddleware.startListening({})`, it attaches a global, long-lived listener tied to the middleware life-cycle.
> 	- it auto cleans on store teardown.
> 	- no manual `stopListening()` needed unless you dynamically register / un-register listeners at runtime.
##### Manual control (for dynamic listeners)
```js
const unsubscribe = listenerMiddleware.startListening({
	actionCreator: someAction,
	effect: async(action, api) => {...}
})

unsubscribe() // return value from listenerMiddleware.startListening
```

