A Higher-Order component (HOC) is a function that takes a component and returns a new enhanced component.

#### Adding authentication to a shopping cart
- want to restrict access to the shopping cart unless the user is logged in.

> [!INFO] Instead of adding authentication logic in every component, we create an HOC that wraps any component that requires authentication.

```js
import { useState, useEffect } from "react";

const withAuth = (WrappedComponent) => {
  return (props) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      const token = localStorage.getItem("token");
      setIsAuthenticated(!!token); // Convert token to boolean
      setLoading(false);
    }, []);

    if (loading) return <p>Loading...</p>; // Prevents flicker during hydration
    return isAuthenticated ? <WrappedComponent {...props} /> : <p>Please log in to continue.</p>;
  };
};

export default withAuth;

```
- this function takes a component (`WrappedComponent`) and returns a new component.
- if the user is authenticated, it renders the original component.
- Otherwise, it shows a login message.

```js
const ShoppingCart = () => {
  return <h2>Your Shopping Cart Items</h2>;
};
```

```js
const ProtectedCart = withAuth(ShoppingCart);
const App = () => {
  return (
    <div>
      <h1>Welcome to the Store</h1>
      <ProtectedCart />
    </div>
  );
};
export default App;
```