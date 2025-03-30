1. Store Configuration (`configureStore`): Simplifies the store creation process by automatically setting up middleware like redux-thunk.
2. State Slices (`createSlice`): A slice is a single unit of Redux state, containing actions and a reducer in one place.
3. Asynchronous Actions (`createAsyncThunk`): Handles async logic, like API requests, with automatic action creation for pending, fulfilled, and rejected states.

> [!INFO] **Immer Integration:** Uses `Immer.js` for writing mutable code that gets converted to immutable updates internally.

