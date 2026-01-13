|#|Feature|Main API(s)|Why It's Essential in React Projects|When / How Often You Use It|
|---|---|---|---|---|
|1|Simplified Store Setup|`configureStore()`|One-line store creation with sensible defaults (Redux Thunk included, DevTools enabled, combine reducers automatically)|Always – root setup|
|2|createSlice|`createSlice()`|Creates reducer + action creators + action types in **one object**. Huge reduction in boilerplate.|Almost every feature/module|
|3|Immer (mutative syntax)|Built into `createSlice` & `createReducer`|Write "mutating" code (`state.value++`) → produces immutable updates safely|Every reducer you write|
|4|Auto-generated Action Creators|From `createSlice()` reducers|No more writing separate action creator functions manually|Every action you dispatch|
|5|Extra Reducers|`extraReducers` in `createSlice`|Clean way to handle thunks, RTK Query, or external actions without switch pollution|Very frequently|
|6|React-Redux Hooks|`useSelector`, `useDispatch`|Official typed hooks → no more `connect()` HOC boilerplate|In every component that reads/dispatches|
|7|createAsyncThunk|`createAsyncThunk()`|Standard way to write async logic (pending/fulfilled/rejected lifecycle actions automatically)|Almost every API call or async side effect|
|8|RTK Query (data fetching & caching)|`createApi()`, `injectEndpoints`|Full-featured alternative to React Query / SWR — endpoints, hooks, caching, polling, invalidation, optimistic updates|Medium/large apps with REST/GraphQL APIs|
|9|Entity Adapter|`createEntityAdapter()`|Normalized state management (CRUD for lists of items) + selectors + memoization|When managing collections (users, todos, products…)|
|10|Reselect-style memoized selectors|`createSelector` from reselect (included)|Efficient derived state computation (prevents unnecessary re-renders)|Whenever you derive/compute from state|
|11|TypeScript-first APIs|Generics & inference everywhere|Excellent type safety with minimal extra typing effort|Strongly recommended in 2025–2026 projects|
|12|DevTools + Time-travel|Included by default in `configureStore`|Automatic integration — inspect, replay, diff state changes|Debugging & development|