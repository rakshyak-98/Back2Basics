[createListenerMiddleware](https://redux-toolkit.js.org/api/createListenerMiddleware)
- it's intended to be a lightweight alternative to more widely used redux async middleware like sagas and observable.

> [!INFO] listener
> - have access to `dispatch` and `getState`, similar to `thunks`

- listeners can be defined statically by calling `listenerMiddleware.startListening()` during setup, or added and removed dynamically at runtime with special `dispatch(addListener())` and `dispatch(removeListener())` actions.

> [!INFO] You must provide exactly _one_ of the four options for deciding when the listener will run: `type`, `actionCreator`, `matcher`, or `predicate`. Every time an action is dispatched, each listener will be checked to see if it should run based on the current action vs the comparison option provided.

```jsx
// 1) Action type string
listenerMiddleware.startListening({ type: 'todos/todoAdded', effect })
// 2) RTK action creator
listenerMiddleware.startListening({ actionCreator: todoAdded, effect })
// 3) RTK matcher function
listenerMiddleware.startListening({
  matcher: isAnyOf(todoAdded, todoToggled),
  effect,
})
// 4) Listener predicate
listenerMiddleware.startListening({
  predicate: (action, currentState, previousState) => {
    // return true when the listener should run
  },
  effect,
})
```

```jsx
import { configureStore, createListenerMiddleware } from '@reduxjs/toolkit'

import todosReducer, {
  todoAdded, 
  todoToggled,
  todoDeleted,
} from '../features/todos/todosSlice'

// Create the middleware instance and methods
const listenerMiddleware = createListenerMiddleware()

// Add one or more listener entries that look for specific actions.
// They may contain any sync or async logic, similar to thunks.
listenerMiddleware.startListening({
  actionCreator: todoAdded,
  effect: async (action, listenerApi) => {
    // Run whatever additional side-effect-y logic you want here
    console.log('Todo added: ', action.payload.text)

    // Can cancel other running instances
    listenerApi.cancelActiveListeners()

    // Run async logic
    const data = await fetchData()

    // Pause until action dispatched or state changed
    if (await listenerApi.condition(matchSomeAction)) {
      // Use the listener API methods to dispatch, get state,
      // unsubscribe the listener, start child tasks, and more
      listenerApi.dispatch(todoAdded('Buy pet food'))

      // Spawn "child tasks" that can do more work and return results
      const task = listenerApi.fork(async (forkApi) => {
        // Can pause execution
        await forkApi.delay(5)
        // Complete the child by returning a value
        return 42
      })

      const result = await task.result
      // Unwrap the child result in the listener
      if (result.status === 'ok') {
        // Logs the `42` result value that was returned
        console.log('Child succeeded: ', result.value)
      }
    }
  },
})

const store = configureStore({
  reducer: {
    todos: todosReducer,
  },
  // Add the listener middleware to the store.
  // NOTE: Since this can receive actions with functions inside,
  // it should go before the serializability check middleware
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().prepend(listenerMiddleware.middleware),
})
```

## Listener management
[listener subscription management](https://redux-toolkit.js.org/api/createListenerMiddleware#listener-subscription-management)