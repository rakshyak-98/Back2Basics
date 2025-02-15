1. Store Configuration (`configureStore`): Simplifies the store creation process by automatically setting up middleware like redux-thunk.
2. State Slices (`createSlice`): A slice is a single unit of Redux state, containing actions and a reducer in one place.
3. Asynchronous Actions (`createAsyncThunk`): Handles async logic, like API requests, with automatic action creation for pending, fulfilled, and rejected states.

> [!INFO] **Immer Integration:** Uses `Immer.js` for writing mutable code that gets converted to immutable updates internally.

**`createSlice`** is a utility function in Redux Toolkit that **automatically generates both actions and a reducer** for you. It simplifies the process of managing state by bundling the actions and reducer logic together.

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