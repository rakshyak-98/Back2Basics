`reducerPath` -> determines where in Redux the data is stored. `providesTags` and `invalidatesTags` -> automatically refresh data when mutations happen.
 - RTK Query is an advanced data fetching and caching tool.
- leverages RTK APIs like [`createSlice`](https://redux-toolkit.js.org/api/createSlice) and [`createAsyncThunk`](https://redux-toolkit.js.org/api/createAsyncThunk) to implement its capabilities. - use of RTK Query's auto-generated React hooks.
- `providersTags: ['products']` -> is used to enable automatic cache invalidation and refetching when related data updates. - If another API mutation updates products and has `invalidatesTags: ['products']` the RTK Query automatically refetch the `getProductByCategoryQuery`
 
 > [!INFO] Query keying
> - RTK Query uses a keying system `queryKey` to store and update API responses.
> - Query keying system ensures different API calls update the correct store data.
> - You don't need to manually manage Redux state-RTK Query handles it for you.

> [!INFO] API calls trigger state update automatically

### Will RTK Query Prevent API calls after page refresh ?
No, RTK Query's cache is stored in memory, so when you refresh the page, the cache is lost, and a new API call is made.

### Dispatching in RTK Query
RTK Query uses `dispatch` to trigger manual refetching or invalidate cached data:

```ts
import { useDispatch } from "react-redux"
import { productApi } from "../redux/productApi"

const RefreshProducts = () => {
	const dispatch = useDispatch();
	const handleRefresh = () => {
		dispatch(productApi.util.invalidateTags(['product']))
	};
	return <button onClick={handleRefresh}> Refresh Products </button>;
}

```
- `invalidateTags(['product'])` -> forces data refetch for updated results.

## Create API slice

> [!INFO] data sync in Redux Store
> - RTK Query stores API response in Redux under `state.api.queries`.

```json
{
  "api": {
    "queries": {
      "getUsers()": {
        "status": "fulfilled",
        "data": [
          { "id": 1, "name": "Alice" },
          { "id": 2, "name": "Bob" }
        ]
      }
    }
  }
}

```

### Feature API slice
```ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { Product } from './types';

export const productApi = createApi({
  reducerPath: 'productApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    getAllProducts: builder.query<Product[], void>({
      query: () => '/products',
    }),
    getProductById: builder.query<Product, number>({
      query: (id) => `/products/${id}`,
    }),
  }),
});

export const { useGetAllProductsQuery, useGetProductByIdQuery } = productApi;

```

# Store
```ts
import { configureStore } from '@reduxjs/toolkit';
import { productApi } from './apiSlice';

export const store = configureStore({
  reducer: {
    [productApi.reducerPath]: productApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(productApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

```
> [!NOTE] You must concat api middleware to `getDefaultMiddleware()` _because RTK Query requires additional middleware for caching, invalidation, and background refetching._

### Fetch data in React Component
```ts
import { useGetAllProductsQuery } from './apiSlice';

const ProductList: React.FC = () => {
  const { data: products, error, isLoading } = useGetAllProductsQuery();

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error loading products</p>;

  return (
    <ul>
      {products?.map((product) => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  );
};

export default ProductList;

```

### `skip` options in RTK Query
- RTK Query provides a `skip` option that prevents the API call until `id` is available
```ts
import { useRouter } from 'next/router';
import { useGetProductByIdQuery } from '../redux/apiSlice';

const ProductDetail = () => {
  const router = useRouter();
  const { id } = router.query; // id is initially undefined

  const { data: product, error, isLoading } = useGetProductByIdQuery(id as string, {
    skip: !id, // Prevents API call until id is available
  });

  if (!id) return <p>Loading...</p>;
  if (isLoading) return <p>Loading product...</p>;
  if (error) return <p>Error loading product</p>;

  return <h1>{product?.name}</h1>;
};

export default ProductDetail;

```

### Example: Auto refetch on Product Addition
```ts
getProductByCategory: builder.query({
	query: (category) => `products?category=${category}`,
	providersTags: ['Products'] // marks data under 'Products'
})

```
- RTK Query sends a POST request.
- `invalidatesTags: ['Products']` tells RTK Query to refetch `getProductByCategory()` automatically.
#### Mutation
```ts
addProduct: builder.mutation({
	query: (newProduct) => ({
		url: "products",
		method: "POST",
		body: newProduct,
	}),
	invalidatesTags: ["Products"],
})
```
- when a new product is added, `invalidatesTags: ['Products']` clears the cache.
- RTK Query automatically refetches `getProductByCategoryQuery`.
- The UI Updates instantly without manual refetching.

| Action                         | What happens in Redux Store                            | UI Update                      |
| ------------------------------ | ------------------------------------------------------ | ------------------------------ |
| `useGetUserQuery()` runs       | Stores response under `state.api.queries.getUsers`     | Shows users list               |
| `useCreateUserMutation()` runs | Invalidates `getUsers` tag -> Auto refresh users again | UI updates with new User       |
| Auto cache                     | Data is stored in Redux for reuse                      | Prevents unnecessary API calls |

## By default, RTK Query does not directly modify other slices of your Redux state. However, you can sync in two main ways
 
### Directly User API cache
Since RTK Query automatically caches API responses, your component should read from `useGetUserQuery()` instead of a separate `UserProfile` state.
```tsx
const {data: userProfile} = useGetUserQuery(userid);

if(userProfile) {
	console.log(userProfile.name); // Data is already in redux store.
}

```

### Sync API data with a separate `UserProfile` slice
if you must store user data separately in `UserProfile`, update it using an extra reducer when `getUser` succeds.
```tsx
import { createSlice, PayloadAction } from '@redux/toolkit';
import { api } from "./api";

interface UserProfile {
	id: number;
	name: string;
	email: string;
}

const initialState: UserProfile | null = null;

export const userSlice = createSlice({
	name: 'userProfile',
	initialState,
	reducers: {} // No standard reducers needed
	extraReducers: (builder) => {
		builder.addMatcher(
			api.endpoints.getUser.matchFulfilled, // when getUserQuery succedds
			(state, action: PayloadAction<UserProfile>) => {
				return action.payload; // updates UserProfile slice
			}
		)
	}
})

export default unserSlice.reducer;

```

> [!NOTE] similar to `createReduer`, the `extraReducer` field uses a _builder callback_ notation to define handlers for specific action types, matching against a range of actions, or handling a default case.
- their are many times that a Redux slice may also need to update its own state in response to actions types that were defined elsewhere in the application (such as clearing many different kinds of data when a __User__ logged out action is dispatched)
	- these can include action types defined by another `createSlice` call, actions generated by a `createAsynThunk` __RTK Query endpoints matchers__  or any other action.

> [!INFO] `extraReducer` allow `createSlice` to respond and update its own state in response to other actions types besides the types it had generated.

> [!WARNING] As with the `reducers` field, each case reducer in `extraReducer` is wrapped 
### Why use `addMatcher()` instead of `addCase()`?
- Both `addMatcher()` and `addCase()` are used in Redux Toolkit `extraReducers` to handle actions outside of the slice (e.g., API responses from RTK Query). However, `addMatcher()` is preferred for RTK Query API actions because of its flexibility.

> [!INFO] `addMatcher`
> - `matchFulfilled` -> triggers when a query / mutation successfully completes (HTTP `2xx` status).
> - `matchRejected` -> triggers when a query / mutation fails (HTTP `4xx` `5xx` etc).
 
### Why add API reducer to Redux store in RTK Query?
when using `createApi` RTK Query, you must add its reducer to the store because Redux toolkit manages all API-related data (cache, loading states, responses) within the redux store.

- RTK Query won't store fetched data in Redux.
- Every request refetches data, ignoring caching benefits.

### How to Persist cache after refresh?
to prevent API calls after refresh, persist Redux state using `redux-persist` [[redux persist]].

```shell
npm install redux-persist
```

```ts
import { configureStore } from "@reduxjs/toolkit";
import { productApi } from "./productApi";
import storage from "redux-persist/lib/storage";
import { persistReducer, persistStore } from "redux-persist";
import { combineReducers } from "redux";

const persistConfig = {
  key: "root",
  storage,
  whitelist: [productApi.reducerPath], // ✅ Persist RTK Query cache
};

const rootReducer = combineReducers({
  [productApi.reducerPath]: productApi.reducer,
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ serializableCheck: false }).concat(productApi.middleware),
});

export const persistor = persistStore(store);

```

#### Wrap the app with `PersistGate`
```ts
import { PersistGate } from "redux-persist/integration/react";
import { persistor, store } from "./store";
import { Provider } from "react-redux";

function MyApp({ Component, pageProps }) {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <Component {...pageProps} />
      </PersistGate>
    </Provider>
  );
}
export default MyApp;

```
- Now RTK query cache persists after refresh!
- No duplicate API calls after page reload.

### Re-fetching on demand with `refetch` `initiate`
[`refetchOnMountOrArgChange`](https://redux-toolkit.js.org/rtk-query/usage/cache-behavior#encouraging-re-fetching-with-refetchonmountorargchange)
- Queries can be encouraged to re-fetch more frequently than usual via the API `refetchOnMountOrArgChange` property.

- refetching on subscription if data exceeds a given time
```ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { Post } from './types'

export const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: '/' }),
  // global configuration for the api
  refetchOnMountOrArgChange: 30,
  endpoints: (build) => ({
    getPosts: build.query<Post[], number>({
      query: () => `posts`,
    }),
  }),
})

```

- refetching at component mount
```ts
import { useGetPostsQuery } from './api'

const Component = () => {
  const { data } = useGetPostsQuery(
    { count: 5 },
    // this overrules the api definition setting,
    // forcing the query to always fetch when this component is mounted
    { refetchOnMountOrArgChange: true },
  )

  return <div>...</div>
}
```

### How does RTK Query Automatically Mange Redux state?
unlike traditional Redux where you manually update state using `dispatch()`, RTK Query automate state management by:
- Auto caching responses -> RTK Query automatically caches API responses based on the query key, if same query is called again, cached data is returned instead of re-fetching.

```js
const { data, isLoading } = useGetUserQuery(userId);

```
- if `userId` remains the same, RTK Query returns cached data instead of making a new request.
- if `userId` changes, it triggers a new API request. No need to manually store or update state. RTK Query manages caching automatically.

- Auto state updates.
- optimistic updates and cache invalidation
- handles loading and error states automatically

### Transform response
[customizing queries](https://redux-toolkit.js.org/rtk-query/usage/customizing-queries#customizing-query-responses-with-transformresponse)

> [!INFO] Individual endpoints on [`createApi`](https://redux-toolkit.js.org/rtk-query/api/createApi) accept a [`transformResponse`](https://redux-toolkit.js.org/rtk-query/api/createApi) property which allows manipulation of the data returned by a query or mutation before it hits the cache.
- `transformResponse` is called with the `meta` property returned from the `baseQuery` as its second argument, which can be used while determining the transformed response. The value for `meta` is dependent on the `baseQuery` used.