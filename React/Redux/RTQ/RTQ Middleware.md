## Create middlewares

```jsx
```

## With Extra Middleware (logger, thunk custom config)

```js
import {} from "@reduxjs/toolkit";
import logger from "redux-logger";

export const store = configureStore({
	reducer: {
		counter: counterRedcuer,
	},
	middleware: (getDefaultMiddleware) =>
		getDefaultMiddleware({
			serializableCheck: true,
			immutableCheck: true,
			thunk: {
				extraArgument: { api: myApliClient },
			}
		}).concat(logger),
		devTool: process.env.NODE_ENV !== 'production',
})
```