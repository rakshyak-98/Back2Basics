- RTK Query is an advanced data fetching and caching tool.
- leverages RTK APIs like [`createSlice`](https://redux-toolkit.js.org/api/createSlice) and [`createAsyncThunk`](https://redux-toolkit.js.org/api/createAsyncThunk) to implement its capabilities.
- use of RTK Query's auto-generated React hooks.
- `providersTags: ['products']` -> is used to enable automatic cache invalidation and refetching when related data updates.
	- If another API mutation updates products and has `invalidatesTags: ['products']` the RTK Query automatically refetch the `getProductByCategoryQuery`

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

### Store
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

### User `skip` options in RTK Query
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

### Example: Auto-refetch on Product Addition
```ts
getProductByCategory: builder.query({
	query: (category) => `products?category=${category}`,
	providersTags: ['Products'] // marks data under 'Products'
})

```

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