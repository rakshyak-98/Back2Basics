in order to update values immutably, your code must make copies of existing objects / array and then modify the copies.

> [!NOTE] A critical rule of immutable updates is that you must make a copy of every level of nesting that needs to be updated.
```js
function handwrittenReducer(state, action) {
  return {
    ...state,
    first: {
      ...state.first,
      second: {
        ...state.first.second,
        [action.someId]: {
          ...state.first.second[action.someId],
          fourth: action.someValue,
        },
      },
    },
  }
}
```

> [!INFO] [[Immer]] is a library that simplifies the process of writing immutable update logic

```js
import { produce } from 'immer'

const baseState = [
  {
    todo: 'Learn typescript',
    done: true,
  },
  {
    todo: 'Try immer',
    done: false,
  },
]

const nextState = produce(baseState, (draftState) => {
  // "mutate" the draft array
  draftState.push({ todo: 'Tweet about it' })
  // "mutate" the nested state
  draftState[1].done = true
})

console.log(baseState === nextState)
// false - the array was copied
console.log(baseState[0] === nextState[0])
// true - the first item was unchanged, so same reference
console.log(baseState[1] === nextState[1])
// false - the second item was copied and updated

```

## Redux Toolkit and Immer
Redux Toolkit's `createReduer` API uses [[Immer]] internally automatically. So, it's already safe to _mutate_ state inside of any case reducer function that is passed to `createReducer`

```js
const todosReducer = createReducer([], (builder) => {
  builder.addCase('todos/todoAdded', (state, action) => {
    // "mutate" the array by calling push()
    state.push(action.payload)
  })
})

```
> [!INFO] `createSlice` uses `createReducer` inside so it's also safe to _mutate_ state there as well

```js
const todosSlice = createSlice({
  name: 'todos',
  initialState: [],
  reducers: {
    todoAdded(state, action) {
      state.push(action.payload)
    },
  },
})

```
- this works because the _mutating_ logic is wrapped in Immer's `produce` method internally when it executes.