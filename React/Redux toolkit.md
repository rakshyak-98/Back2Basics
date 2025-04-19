1. Store Configuration (`configureStore`): Simplifies the store creation process by automatically setting up middleware like redux-thunk.
2. State Slices (`createSlice`): A slice is a single unit of Redux state, containing actions and a reducer in one place.
3. Asynchronous Actions (`createAsyncThunk`): Handles `async` logic, like API requests, with automatic action creation for pending, fulfilled, and rejected states.

> [!INFO] **Immer Integration:** Uses `Immer.js` for writing mutable code that gets converted to immutable updates internally.

> [!INFO] Many ESLint configs include the [no-param-reassign](https://eslint.org/docs/rules/no-param-reassign) rule, which may also warn about mutations to nested fields. 

> [!WARNING] In Immer powered reducers, no-param-reassign is not helpful
- To resolve this, you can tell the ESLint rule to ignore mutations and assignment to a parameter named `state` only in slice files:
```js
// @filename .eslintrc.js
module.exports = {
  // add to your ESLint config definition
  overrides: [
    {
      // feel free to replace with your preferred file pattern - eg. 'src/**/*Slice.ts'
      files: ['src/**/*.slice.ts'],
      // avoid state param assignment
      rules: { 'no-param-reassign': ['error', { props: false }] },
    },
  ],
}

```

### Cross component state sync
any component using `useSelector()` auto-subscribe to the store. When the slice updates, all connected components re-render.

### What Triggers re-render?
- Component uses `useSelector(...)`.
- Selector returns new references or different value.
- Redux store emits change -> selector runs -> value changed -> re-render.
- not splitting state into multiple slices.

```js
const selectorItems = createSelector(state => state.itmes, items => items)
const items = useSelector(selectItems)
```

### Sync state across multiple slices

> [!INFO] each slice is isolated -> can't modify another slice

### Sync via

##### Share action pattern
```js
// actions/globalActions.js
import {createAction} from "@reduxjs/toolkit";
export const userLoggedOut = createAction("use/logout")
```

```js
// userSlice.js

import { useLoggedOut } from "../actions/globalActions";
extraReducers: (builder) => {
	builder.addCase(userLoggedOut, (state) => {
		state.info = null;
	})
}

```

```js
// settingSlice.js

extraReducers: (builder) => {
	builder.addCase(userLoggedOut, (state) => {
		state.theme = 'light'
	})
}

```

#### Create listener middleware (RTK-native)
> [!INFO] prefer `listenerMiddleware` or central orchestration logic.

|                                                          |     |
| -------------------------------------------------------- | --- |
| Prefer listenerMiddleware or central orchestration logic |     |

```js
import { createListenerMiddleware } from "@reduxjs/toolkit"
import { userLoggedOut} from "./actions/globalActions"

const listenerMiddleware = createListenerMiddleware();

listenerMiddleware.startListening({
	actionCreator: userLoggedOut,
	effect: async (actions, listenerApi) => {
		listenerApi.dispatch(clearCache());
		listenerApi.dispatch(resetForms());
	}
})

```

```js
// store.js

configureStore({
	reducer: {},
	middleware: (getDefault) => getDefault().prepend(listenerMiddleware.middleware)
})

```

### Sync API slice

```js
import { myAPi } from "../services/myApi"

extraReduers: (builder) => {
	builder.addMather(
		myApi.endpoints.getUser.matchFulfilled,
		(state, action) => {
			state.user = actions.payload
		}
	)
}

```

- `onQueryStarted` hook (preferred for side effects dispatch)
```ts
getUser: builder.query<User, void>({
	async onQueryStarted(_, {dispatch, queryFulfilled}){
		try{
			const { data } = await queryFulfilled;
			dispatch(userSlice.actions.setUsers(data))
		}catch {}
	}
})

```

###### create listener middleware
```ts
listenerMiddleware.startListening({
	matcher: myAPi.endpoints.getUser.matchFulfilled,
	effect: async (action, api) => {
		api.dispatch(setUser(action.payload))
	}
})

```
