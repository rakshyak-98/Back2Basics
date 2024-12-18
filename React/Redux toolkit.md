1. Store Configuration (`configureStore`): Simplifies the store creation process by automatically setting up middleware like redux-thunk.
2. State Slices (`createSlice`): A slice is a single unit of Redux state, containing actions and a reducer in one place.
3. Asynchronous Actions (`createAsyncThunk`): Handles async logic, like API requests, with automatic action creation for pending, fulfilled, and rejected states.

> [!INFO] **Immer Integration:** Uses `Immer.js` for writing mutable code that gets converted to immutable updates internally.

**`createSlice`** is a utility function in Redux Toolkit that **automatically generates both actions and a reducer** for you. It simplifies the process of managing state by bundling the actions and reducer logic together.

```javascript
import { createSlice } from '@reduxjs/toolkit';

// This is the `createSlice` function that combines both actions and a reducer.
const counterSlice = createSlice({
  name: 'counter', // Name of the slice (used in action types)
  initialState: { value: 0 }, // Initial state of the slice

  // Reducers section: defines the state update logic
  reducers: {
    // Action: 'increment'
    // Reducer: Updates state by incrementing the value
    increment: (state) => {
      state.value += 1;
    },

    // Action: 'decrement'
    // Reducer: Updates state by decrementing the value
    decrement: (state) => {
      state.value -= 1;
    },

    // Action: 'incrementByAmount'
    // Reducer: Updates state based on action.payload
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    },
  },
});

// **Actions** - Auto-generated from the reducer functions
export const { increment, decrement, incrementByAmount } = counterSlice.actions;

// **Reducer** - Auto-generated reducer function that handles state updates
export default counterSlice.reducer;
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