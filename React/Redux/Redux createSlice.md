## Creating slice
**`createSlice`** is a utility function in Redux Toolkit that **automatically generates both actions and a reducer** for you. It simplifies the process of managing state by bundling the actions and reducer logic together.

[!INFO] `createSlice` and `createReducer` automatically use [[Immer]] internally to let you write simpler immutable update logic using _mutating_ syntax.

> [!INFO] `createReducer` and `createSlice` automatically use [[Immer]]
> [!INFO] `name` required in `createSlice` to auto generate action types
> - `name` property is used as a prefix for action types.
> - ensure uniqueness in redux state.
> - clearly shows action names in redux devtools.

```js
import { configureStore } from '@redux/toolkit'
import { api } from './api'

export const store = configureStore({
	reducer: {
		[api.reducerPath]: api.reducer,
	},
	middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(api.middleware)
})

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

```

> [!Note] mutating state in an arrow function with an implicit return breaks this rule and causes an error!
```js
const todosSlice = createSlice({
  name: 'todos',
  initialState: {todos: [], status: 'idle'}
  reducers: {
    todoDeleted(state, action.payload) {
      // Construct a new array immutably
      const newTodos = state.todos.filter(todo => todo.id !== action.payload)
      // "Mutate" the existing state to save the new array
      state.todos = newTodos
    }
  }
})

```
- This is because statements and function calls may return a value, and Immer sees both the attempted mutation and _and_ the new returned value and doesn't know which to use as the result.

> [!INFO] slice reducer 
> - `extraReduer` -> what are the thing this slice is not in charge of that it might to deal with.

> [!NOTE] As an alternative, you can use `Object.assign` to mutate multiple fields at once, since `Object.assign` always mutates the first object that it's given. [ref](https://redux-toolkit.js.org/usage/immer-reducers)
```js
function objectCaseReducer3(state, action) {
  const { a, b, c, d } = action.payload
  Object.assign(state, { a, b, c, d })
}

```

```ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Define the state type
interface CounterState {
  value: number;
}

// Define the initial state
const initialState: CounterState = {
  value: 0,
};

// Create the Redux slice with type safety
const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;

```

```ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  totalAmount: number;
}

const initialState: CartState = {
  items: [],
  totalAmount: 0,
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addItem: (state, action: PayloadAction<CartItem>) => {
      const existingItem = state.items.find(item => item.id === action.payload.id);
      if (existingItem) {
        existingItem.quantity += action.payload.quantity;
      } else {
        state.items.push(action.payload);
      }
      state.totalAmount += action.payload.price * action.payload.quantity;
    },
    removeItem: (state, action: PayloadAction<string>) => {
      const index = state.items.findIndex(item => item.id === action.payload);
      if (index !== -1) {
        state.totalAmount -= state.items[index].price * state.items[index].quantity;
        state.items.splice(index, 1);
      }
    },
    updateQuantity: (state, action: PayloadAction<{ id: string; quantity: number }>) => {
      const item = state.items.find(item => item.id === action.payload.id);
      if (item) {
        state.totalAmount += (action.payload.quantity - item.quantity) * item.price;
        item.quantity = action.payload.quantity;
      }
    },
    clearCart: (state) => {
      state.items = [];
      state.totalAmount = 0;
    },
  },
});

export const { addItem, removeItem, updateQuantity, clearCart } = cartSlice.actions;
export default cartSlice.reducer;

```
- the Redux store requires a reducer, not the whole slice. that is why we have this `export default cartSlice.reducer`

### Updating Nested Data

> [!INFO] There may be occasions when you want to insert a value and then make further updates to it.
Related to this RTK's `createEntityAdapter` update function can either be used as standalone reducers, or _mutating_ update functions.

### Keep slice in sync
- when one slice updates, the other should respond accordingly.

> [!NOTE] cannot directly access another slice's state inside a reducer.
- use `extraReducers` `createAction` or `createAsyncThunk`

```js
// userThunk.ts
export const loginUser = createAsyncThunk('user/login', async (creds, { dispatch }) => {
  const user = await api.login(creds);
  dispatch(userLoggedIn({ userId: user.id }));
  dispatch(syncProfile({ userId: user.id })); // <- runs after user state is updated
  return user;
});

```

> [!WARNING] You cannot access same slice reducer in `extraReducers` property

```js
extraReducers: (builder) => {
  builder.addCase(mySlice.actions.doSomething, ...) // ❌ won't work
}

```

if you need to run an action Workaround
```js
export const doSomething = createAction('mySlice/doSomething');

createSlice({
  name: 'mySlice',
  initialState,
  reducers: {}, // or use it here too
  extraReducers: (builder) => {
    builder.addCase(doSomething, (state) => {
      state.count++;
    });
  },
});

```

> [!INFO] `extraReducers` are designed to respond to actions defined outside the slice or to handle async actions, and do not have internal access to the slice's reducer functions

## What are selectors
extract the transform specific pieces of state from the Redux store.

Memoization
caches function results based on input args.

### `reselect`/`createSelector`
`createSelector` from `reselect` or RTK does memoization automatically.

```js
import { createSelector } from "reselect"

const selectTodos = (state) => state.todos.items;

const selectIncompleteTodos = createSelector([selectTodos], (todos) => todos.filter(todo => !todo.completed));
```
- First args: input selector(s)
- Second args: transform logic (only re-runs if input changes)
- helps to move logic (filtering, mapping, computations) out of components. Avoid scattered business logic across components.
