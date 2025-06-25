```shell
npm install @reduxjs/toolkit react-redux
```

Reducers -> listen for dispatched actions and modify the store.
Dispatching -> triggers state updates in Redux.

> [!INFO] You don't have to use actions manually with Redux Toolkit (RTK) in most cases.
> - RTK Provides `createSlice` and RTK Query, which automatically generate actions for you.
> - RTK automatically generates actions for reducers.
### Dispatching
Dispatching in Redux means sending an action to the redux store to update the state.
- you dispatch an action -> the reducer process it -> the store update the state.

- A Redux application state tree is an *immutable data structure*.  It will not change as long as it exists. It will keep holding the same state forever. How you then go to the next state is by producing another state tree that reflects the changes you wanted to make.
- Replacing things in maps, removing things from array etc. However, this is not how things are done in Redux.

> non-destructive updates, you can hold on to the history of your application state without doing much extra work: Just keep a collection of the previous state trees around. You can then do things like undo/redo for "free". so that you can replay it later, which can he hugely helpful when debugging.
### Redux tool kit
- solve the problem where an action in a slice return an immutable state
```javascript
import {createSlice} from "@reduxjs/toolkit"
const initState = {value : 0}
const counter = createSlice({
	name: "counter", // important requirend redux use it internally
	initState,
	reducers : {
		incremented(state, _){
			// return { ...state }
			state.value++; // instead above we can use like this (It's Reduxjs)
		}
	}
})
```

>[!INFO] uses library called [immer](https://www.npmjs.com/package/immer)

```js
import { getDefaultMiddleware } from "@reduxjs/toolkit"

const middleware = getDefaultMiddleware 
```

`getDefaultMiddleware` is a utility function provided by Redux Toolkit to configure a store with a set of default middlewares.
	- It ensures that essential middleware like `redux-thunk`, `serilizaleStateInvariantMiddleware`, and `immutableStateInvariantMiddleware` are automatically added.

`redux-thunk` -> allows `async` logic (e.g, API calls) in actions. 
`serilizaleStateInvariantMiddleware` -> Ensures state is serializable (development only).
`immutableStateInvariantMiddleware` -> Prevents accidental state mutations (development only).

#### What does "Ensure state is serializable" means?
In redux, the state should be serializable, meaning it can be converted into a format like JSON and stored or transferred without losing its structure or meaning.

#### Why should state be serializable?
- Ensure state updates are trackable.
- tools like Redux DevTools rely on serializable state to replay actions.
- Helps store state in `localStore` or send it to a server.
- Time-travel debugging -> enables stepping forward and backward in state changes.

#### How to fix serialization issues?
```js
{user: new Map()}; # Bad
{user: Object.fromEntries(userMap)};

{lastLogin: new Date()}
{lastLogin: Date.now()}
```


> [!INFO] [[redux persist]] is a library that automatically saves and rehydrates the Redux state to/from `localStorage` `sessionStorage`, or `IndexedDB`
- rehydrates -> Restores state from storage when the app reloads.

### setup listeners
A utility used to enable `refetchOnFocus` and `refetchOnReconnect` behaviors. It requires the `dispatch` method from your store.
- calling `setupListeners(store.dispatch)` will configure listeners with the recommended defaults, but you have the option of providing a callback for more granular control.
