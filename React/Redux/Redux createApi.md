	Like the Redux core and Redux Toolkit, RTK Query's primary functionality is UI-agnostic and can be used with any UI layer. RTK Query also includes a version of [`createApi`](https://redux-toolkit.js.org/rtk-query/api/createApi) designed specifically for use with React, which [automatically generates React hooks](https://redux-toolkit.js.org/rtk-query/api/created-api/hooks).

> [!INFO] `ApiProvider`
> Can be used as a `Provider` if you **do not already have a Redux store**.
> [ApiProvider](https://redux-toolkit.js.org/rtk-query/api/ApiProvider)
> 
```js
import * as React from 'react';
import { ApiProvider } from '@reduxjs/toolkit/query/react';
import { Pokemon } from './features/Pokemon';

function App() {
  return (
    <ApiProvider api={api}>
      <Pokemon />
    </ApiProvider>
  );
}
```

> [!NOTE] `fetchBaseQuery`
> By default, `fetchBaseQuery` assumes that every request you make will be `json`, so in those cases all you have to do is set the `url` and pass a `body` object when appropriate.
> [parsing response](https://redux-toolkit.js.org/rtk-query/api/fetchBaseQuery#parsing-a-response)
> [adding custom timeout](https://redux-toolkit.js.org/rtk-query/api/fetchBaseQuery#adding-a-custom-timeout-to-requests)

```ts
import { createSlice, PayloadAction, createAsyncThunk, createApi, fetchBaseQuery } from '@reduxjs/toolkit';

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

export const cartApi = createApi({
  reducerPath: 'cartApi', // this determines where the API data is stored in Redux.
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
	tagTypes: ['Users'] // Define a tag for cache nivalidation.
  endpoints: (builder) => ({
    fetchCart: builder.query<CartItem[], void>({
      query: () => '/cart',
			providesTags: ['Users'], // This marks tha data with the "Users" tag
    }),
    addItem: builder.mutation<CartItem, CartItem>({
      query: (item) => ({
        url: '/cart',
        method: 'POST',
        body: item,
      }),
			invalidatesTags: ['Users'] // this invalidates "Users" tag, triggering a refresh of getUsers.
    }),
    removeItem: builder.mutation<void, string>({
      query: (id) => ({
        url: `/cart/${id}`,
        method: 'DELETE',
      }),
    }),
  }),
});

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
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

// [ for api slice ]
export const { useFetchCartQuery, useAddItemMutation, useRemoveItemMutation } = cartApi;

// [ for state slice ]
export const { updateQuantity, clearCart } = cartSlice.actions;
export default cartSlice.reducer;

```

### Difference Between Action and Reducer in Redux

| **Aspect**       | **Action**                                                                    | **Reducer**                                                              |
| ---------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Definition**   | An object that describes **what** happened.                                   | A function that specifies **how** the state changes based on the action. |
| **Purpose**      | Represents an **intention** to change the state.                              | Handles the **actual state update** based on the action type.            |
| **Content**      | Contains a `type` (mandatory) and an optional `payload` with additional data. | Takes the current state and an action, returns the new state.            |
| **Example**      | `{ type: 'INCREMENT', payload: 1 }`                                           | `(state, action) => { return { count: state.count + 1 } }`               |
| **Usage**        | Created and dispatched to trigger state changes.                              | Listens for actions and updates the state accordingly.                   |
| **Side Effects** | None, just describes an event.                                                | Pure function: must not have side effects.                               |

---

### Example

1. **Action:**
```javascript
// Action object
const incrementAction = { type: 'INCREMENT', payload: 1 };
```

2. **Reducer:**
```javascript
// Reducer function
const counterReducer = (state = { count: 0 }, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + action.payload };
    default:
      return state;
  }
};
```

**Explanation:**
- The **action** describes **what** happened (`INCREMENT` by `1`).
- The **reducer** handles **how** the state is updated (increments `count` by `1`).

---

### Summary
- **Actions** are "messages" that carry information about an event.
- **Reducers** define the logic to update the state based on the action type.

### Manually refresh query

```jsx
import { useGetUserQuery, useCreateUserMutation } from "./api"

const AddUser = () => {
	const { refresh } = useGetUserQuey();
	const [ createUser ] = useCreateUserMutation();

	const handleAddUser = async () => {
		await createUser({ name: 'New User' })
		refresh();
	}

	return <button onClick={handleAddUser}>Add User</button>;
}
```

#### Auto invalidate cache

```jsx
endPoints: (builder) => ({
	createUser: builder.mutation<User, Partial<User>>({
		query: (newUser) => ({
			url: 'users',
			method: "POST",
			body: newUser,
		}),
		invalidatesTags: ['Users'],
	}),
	getUsres: builder.query<User[], void>({
		query: () => 'users',
		providesTags: ['Users'],
	})
})

```
- Now, after `createUser()` RTK Query automatically refetches `getUsers` keeping the store updated.

##### manually accessing API data from Redux
```jsx
import { useSelector } from "react-redux";
import { api } from "./api";

const users = useSelector((state) => api.endpoints.getUsers.select(state)?.data);
```