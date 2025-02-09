### API Service layer

```js
import axios from 'axios';

const apiClient = axios.create({
	baseURL: process.env.BASE_URL,
	timeout: 10000,
	haders: { "Content-Type": "application/json" },
})

apiClint.interceptos.request.use(
	(config) => {
		config.headers.Authorization = `Bearer ${localStorage.getItem("token")}`;
		return config;
	},
	(error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
	(response) => response.data,
	async (error) => {
		if(error.response?.status === 401){
			// Handle token refresh or logout
		}
		return Promise.reject(error);
	}
)

export default apiClient;
```

### Data fetching layer (React Query hook)

```js
import { userQuery } from "@tanstack/request/query"
import apiClient from "./apiClient"

const FIVE_MINUTES = 5 * 60 * 1000
const NO_OF_RETRY = 2

const fetchProducts = async () => {
	return await apiClient.get("/products")
}

export const useProducts = () => {
	return useQuery({
		queryKey: ["products"],
		queryFn: fetchProducts,
		staleTime: FIVE_MINUTES, // Cache data form 5 min
		refetchOnWindowsFocus: false,
		retry: NO_OF_RETRY,
	})
}

```
- Encapsulate data fetching logic with caching, re-validation, background update.

### UI component
```jsx
import { useProducts } from "@hooks/useProducts";

const ProductList = () => {
	const { data, isLoading, isError } = useProduct();
	if(isLoading) return <p> Loading... </p>;
	if(isError) return <p>Failed to load products.</p>;

	return (
		<ul>
			{data.map((product) => {<li key={product.id}>{product.name}</li>})}	
		</ul>
	)
}
export default ProductList;

```
