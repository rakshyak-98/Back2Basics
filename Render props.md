- A render prop is a function prop that component uses to share reusable logic.
- Instead of wrapping components (like HOCs), the parent component controls rendering.
- Used for logic reuse, such as authentication, state management, and event handling.

Instead of maintaining cart state in multiple places, we create a CartProvider component that shares cart logic via a render prop.

```jsx
import { useState } from "react";

const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);

  const addItem = (item) => setCart([...cart, item]);
  const removeItem = (id) => setCart(cart.filter((item) => item.id !== id));

  return children({ cart, addItem, removeItem });
};

export default CartProvider;

```
##### With context API
```jsx
import { createContext, useState, useContext } from "react";

const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);

  const addItem = (item) => setCart([...cart, item]);
  const removeItem = (id) => setCart(cart.filter((item) => item.id !== id));

  return (
    <CartContext.Provider value={{ cart, addItem, removeItem }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);

```

```jsx
const ShoppingCart = () => {
  return (
    <CartProvider>
      {({ cart, addItem, removeItem }) => (
        <div>
          <h2>Your Shopping Cart</h2>
          {cart.length === 0 ? <p>Cart is empty</p> : null}
          <ul>
            {cart.map((item) => (
              <li key={item.id}>
                {item.name} <button onClick={() => removeItem(item.id)}>Remove</button>
              </li>
            ))}
          </ul>
          <button onClick={() => addItem({ id: Date.now(), name: "New Item" })}>
            Add Item
          </button>
        </div>
      )}
    </CartProvider>
  );
};

export default ShoppingCart;

```

##### Using the context
```jsx
import { useCart } from "./CartContext";

const ShoppingCart = () => {
  const { cart, addItem, removeItem } = useCart();

  return (
    <div>
      <h2>Your Shopping Cart</h2>
      {cart.length === 0 ? <p>Cart is empty</p> : null}
      <ul>
        {cart.map((item) => (
          <li key={item.id}>
            {item.name} <button onClick={() => removeItem(item.id)}>Remove</button>
          </li>
        ))}
      </ul>
      <button onClick={() => addItem({ id: Date.now(), name: "New Item" })}>
        Add Item
      </button>
    </div>
  );
};

export default ShoppingCart;

```
