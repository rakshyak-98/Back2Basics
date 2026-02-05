
## Store

### attach api react query slice (`createApi`)

```ts
import { configureStore } from '@reduxjs/toolkit';
import { productApi } from './apiSlice';
import { setupListeners } from "@reduxjs/toolkit/query";

export const store = configureStore({
  reducer: {
    [productApi.reducerPath]: productApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(productApi.middleware),
});

setupLinsteners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

```
> [!NOTE] You must concat api middleware to `getDefaultMiddleware()` _because RTK Query requires additional middleware for caching, invalidation, and background refetching._

> [!INFO]
> `setupLinsteners(store.dispatch);` -> if you're using RTK Query and want polling, auto-refetch on tab focus, or reconnection handling to work automatically -> you need this line.
> - it attaches several global event listeners to the store's dispatch pipeline. These listeners react to certain actions and automatically trigger usefull side-effects.

### Config when you want Maximum Control

```jsx
export const store = configureStore({
	reducer: rootReducer, // or combineReducers({...})
	
	middleware: (getDefaultMiddleware) => [
		...getDefaultMiddleware({
		}),
		customMiddlewareA,
		customMiddlewareB,
	]
})
```


### What `setupLinsteners(store.dispatch);` actually does

|Behavior|What happens without `setupListeners`|What happens with `setupListeners`|Why most people need it|
|---|---|---|---|
|**Automatic refetch on focus**|Nothing|Refetches all active queries when window gets focus|Very useful in tabs / multi-window apps|
|**Automatic refetch on network reconnect**|Nothing|Refetches when navigator.onLine becomes true again|Handles spotty Wi-Fi, airplane mode, etc.|
|**Automatic refetch on mount / argument change**|Works, but only basic cases|More consistent timing & conditions|Usually not the main reason|
|**Polling** (when `pollingInterval` is set)|Polling does **not** start|Starts/stops polling automatically|Critical if you use polling anywhere|
|**Cache entry lifecycle events**|Some internal cleanup may be delayed|Cache entries are garbage-collected more reliably|Helps prevent memory leaks in long-running apps|

> [!NOTE] Most common reasons people notice it's missing
> - They turned on `pollingInterval: 3000` in some endpoint
> - They switch browser tabs or disconnect/reconnect internet. Data stays stale, no automatic background refresh.

### Can you turn some behavior off

```jsx
setupListeners(store.dispatch, {
  refetchOnFocus: false,          // default = true
  refetchOnReconnect: false,      // default = true
  refetchOnMountOrArgChange: true // default = false (more aggressive)
})
```