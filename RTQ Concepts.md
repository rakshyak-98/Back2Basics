## Redux Toolkit (RTK) — Full Feature Reference

### 1. `configureStore()`

Wraps `createStore` to provide simplified configuration with good defaults — automatically combines slice reducers, adds middleware, includes `redux-thunk` by default, and enables the Redux DevTools Extension.

```js
import { configureStore } from '@reduxjs/toolkit'

const store = configureStore({
  reducer: {
    // your slice reducers go here
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(/* custom middleware */),  // extend defaults
  preloadedState: {},     // optional initial state (for SSR / hydration)
  enhancers: (getDefaultEnhancers) =>
    getDefaultEnhancers().concat(/* custom enhancers */),
  devTools: true,         // auto-disabled in production
})
```

---

### 2. `createSlice()`

The cornerstone of RTK — bundles reducer + actions together. Uses **Immer** internally so you can write "mutating" logic safely.

```js
import { createSlice } from '@reduxjs/toolkit'

const mySlice = createSlice({
  name: 'featureName',        // prefix for action types
  initialState: {},           // initial state shape
  reducers: {
    // each key becomes an action creator AND a case reducer
    someAction(state, action) {
      // mutate state directly — Immer handles immutability
    },
    // use prepare callback to customize action payload
    actionWithPrepare: {
      reducer(state, action) { /* ... */ },
      prepare(arg) { return { payload: /* transform arg */ } }
    }
  },
  extraReducers: (builder) => {
    // handle actions from OTHER slices or createAsyncThunk
    builder
      .addCase(/* externalAction */, (state, action) => {})
      .addMatcher(/* matchFn */, (state, action) => {})
      .addDefaultCase((state, action) => {})
  },
  selectors: {
    // define co-located selectors (RTK 2.0+)
    selectSomething: (state) => state.something
  }
})

export const { someAction } = mySlice.actions
export default mySlice.reducer
```

---

### 3. `createReducer()`

A standalone reducer builder — useful when not using `createSlice`.

```js
import { createReducer } from '@reduxjs/toolkit'

const reducer = createReducer(initialState, (builder) => {
  builder
    .addCase(actionCreator, (state, action) => {
      // Immer-powered — mutate freely
    })
    .addMatcher(
      (action) => action.type.endsWith('/pending'), // match predicate
      (state) => { /* handle matched actions */ }
    )
    .addDefaultCase((state) => { /* fallback */ })
})
```

---

### 4. `createAction()`

Generates a typed action creator with less boilerplate.

```js
import { createAction } from '@reduxjs/toolkit'

const increment = createAction('counter/increment')
// increment()         → { type: 'counter/increment' }
// increment.type      → 'counter/increment'
// increment.toString()→ 'counter/increment' (useful in switch/addCase)

// With payload transformer:
const addItem = createAction('cart/add', (item) => ({
  payload: { ...item, addedAt: Date.now() }
}))
```

---

### 5. `createAsyncThunk()`

Handles async logic (API calls, etc.) and auto-dispatches `pending / fulfilled / rejected` actions.

```js
import { createAsyncThunk } from '@reduxjs/toolkit'

const fetchUser = createAsyncThunk(
  'users/fetchById',          // action type prefix
  async (userId, thunkAPI) => {
    // thunkAPI: { dispatch, getState, rejectWithValue, signal, ... }
    try {
      const data = await api.getUser(userId)
      return data                          // → fulfilled payload
    } catch (err) {
      return thunkAPI.rejectWithValue(err) // → rejected payload
    }
  },
  {
    condition: (arg, { getState }) => {
      // optionally cancel if condition is false
    }
  }
)

// In your slice's extraReducers:
// fetchUser.pending   / fetchUser.fulfilled / fetchUser.rejected
```

---

### 6. `createEntityAdapter()`

Manages normalized collections (arrays of objects with IDs) with built-in CRUD helpers.

```js
import { createEntityAdapter } from '@reduxjs/toolkit'

const usersAdapter = createEntityAdapter({
  selectId: (user) => user.id,           // default is entity.id
  sortComparer: (a, b) => a.name.localeCompare(b.name) // optional sort
})

// Generated state shape: { ids: [], entities: {} }
const initialState = usersAdapter.getInitialState({
  loading: false  // extend with extra fields
})

// CRUD operations (use inside createSlice reducers):
// usersAdapter.addOne(state, entity)
// usersAdapter.addMany(state, entities)
// usersAdapter.setOne / setMany / setAll
// usersAdapter.updateOne(state, { id, changes })
// usersAdapter.upsertOne / upsertMany
// usersAdapter.removeOne(state, id)
// usersAdapter.removeMany / removeAll

// Auto-generated selectors:
const selectors = usersAdapter.getSelectors((state) => state.users)
// selectors.selectAll / selectById / selectIds / selectEntities / selectTotal
```

---

### 7. `createSelector()` (via Reselect)

Memoized selectors — recomputes only when inputs change.

```js
import { createSelector } from '@reduxjs/toolkit'

const selectUsers = (state) => state.users.entities
const selectFilter = (state) => state.filter.value

const selectFilteredUsers = createSelector(
  [selectUsers, selectFilter],         // input selectors
  (users, filter) => {                 // result function (memoized)
    return users.filter(u => u.name.includes(filter))
  }
)
```

---

### 8. `combineSlices()` _(RTK 2.0+)_

Enables lazy-loading of reducers at runtime — designed to support code splitting and reducer injection patterns.

```js
import { combineSlices } from '@reduxjs/toolkit'

const rootReducer = combineSlices(
  sliceA,
  sliceB,
  // inject slices lazily later with rootReducer.inject(slice)
)
```

---

### 9. `createDynamicMiddleware()` _(RTK 2.0+)_

Allows dynamically adding middleware to the store at runtime — useful for code splitting. Includes a React hook that automatically adds a middleware and returns the updated dispatch.

```js
import { createDynamicMiddleware, configureStore } from '@reduxjs/toolkit'

const dynamicMiddleware = createDynamicMiddleware()

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().prepend(dynamicMiddleware.middleware)
})

// Add middleware later at runtime:
dynamicMiddleware.addMiddleware(myLazyMiddleware)

// React hook integration:
// const dispatch = dynamicMiddleware.createDispatchWithMiddlewareHook(myMiddleware)
```

---

### 10. RTK Query — `createApi()`

A powerful, optional data fetching and caching capability built into RTK — eliminates the need to hand-write data fetching and caching logic.

```js
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const myApi = createApi({
  reducerPath: 'myApi',                        // key in Redux store
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['User', 'Post'],                  // for cache invalidation
  keepUnusedDataFor: 60,                       // seconds (global default)
  endpoints: (builder) => ({

    // Query endpoint (GET / read)
    getUser: builder.query({
      query: (id) => `/users/${id}`,
      providesTags: ['User'],                  // cache tag
      transformResponse: (response) => response.data,
    }),

    // Mutation endpoint (POST/PUT/DELETE / write)
    updateUser: builder.mutation({
      query: ({ id, ...body }) => ({
        url: `/users/${id}`,
        method: 'PUT',
        body,
      }),
      invalidatesTags: ['User'],               // auto refetch on success
    }),

    // Infinite query / paginated (RTK 2.0+)
    getPage: builder.infiniteQuery({
      query: ({ pageParam }) => `/items?page=${pageParam}`,
      infiniteQueryOptions: {
        initialPageParam: 1,
        getNextPageParam: (lastPage) => lastPage.nextPage
      }
    })
  })
})

// Auto-generated React hooks:
// useGetUserQuery(id)
// useUpdateUserMutation()
// useGetPageInfiniteQuery(...)
```

---

### 11. RTK Query — `fetchBaseQuery` & Custom Base Queries

```js
import { fetchBaseQuery } from '@reduxjs/toolkit/query'

const baseQuery = fetchBaseQuery({
  baseUrl: 'https://api.example.com',
  prepareHeaders: (headers, { getState }) => {
    // attach auth token to every request
    const token = getState().auth.token
    if (token) headers.set('Authorization', `Bearer ${token}`)
    return headers
  },
})

// Wrap with re-authentication logic using fetchBaseQueryWithReauth pattern
```

---

### 12. RTK Query — OpenAPI Codegen _(RTK 2.0+)_

Generates typed RTK Query endpoints from an OpenAPI definition, with support for regex patterns and explicit tag overrides via a codegen config.

```bash
# Install codegen tool
npx @rtk-query/codegen-openapi openapi-config.ts

# openapi-config.ts template:
# {
#   schemaFile: './openapi.json',      // or URL
#   apiFile: './src/store/emptyApi.ts',
#   outputFile: './src/store/generatedApi.ts',
#   exportName: 'generatedApi',
#   hooks: true,                       // generate React hooks
#   tag: true,                         // use OpenAPI tags for grouping
# }
```

---

### 13. Immer Integration (Built-in)

Every `createSlice` and `createReducer` uses Immer automatically.

```js
// No need to spread — just mutate:
reducers: {
  addItem(state, action) {
    state.items.push(action.payload) // ✅ safe mutation
  },
  clearItems(state) {
    return []  // ✅ can also return a new value
  }
}
```

---

### Summary Table

| Feature                   | Purpose                               |
| ------------------------- | ------------------------------------- |
| `configureStore`          | Store setup with sane defaults        |
| `createSlice`             | Reducer + actions in one              |
| `createReducer`           | Standalone reducer with Immer         |
| `createAction`            | Typed action creator                  |
| `createAsyncThunk`        | Async logic + lifecycle actions       |
| `createEntityAdapter`     | Normalized data + CRUD helpers        |
| `createSelector`          | Memoized selectors (Reselect)         |
| `combineSlices`           | Lazy/code-split reducers (2.0+)       |
| `createDynamicMiddleware` | Runtime middleware injection (2.0+)   |
| `createApi` (RTK Query)   | Data fetching + caching layer         |
| `fetchBaseQuery`          | Built-in fetch wrapper for RTK Query  |
| OpenAPI Codegen           | Auto-generate endpoints from schema   |
| Immer (built-in)          | Immutable updates via mutation syntax |