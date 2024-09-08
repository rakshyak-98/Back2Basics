```typescript vite.d.ts
/// <reference types="vite/client" />
/// <reference types="react" />
/// <reference types="node" />
```
- Remember, for this to work, you need to have the corresponding `@types` packages installed in your project. For instance, `@types/react` for React types or `@types/node` for Node.js types.
- This method is particularly useful for including ambient type declarations that don't get automatically picked up by TypeScript's module resolution system.

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