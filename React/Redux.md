- A Redux application state tree is an *immutable data structure*.  It will not change as long as it exists. It will keep holding the same state forever. How you then go to the next state is by producing another state tree that reflects the changes you wanted to make.
- Replacing things in maps, removing things from array etc. However, this is not how things are done in Redux.

> non-destructive updates, you can hold on to the history of your application state without doing much extra work: Just keep a collection of the previous state trees around. You can then do things like undo/redo for "free". so that you can replay it later, which can he hugely helpful when debugging.
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