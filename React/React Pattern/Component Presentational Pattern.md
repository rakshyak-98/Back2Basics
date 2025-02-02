## Why use this pattern?
- Logic (Container) is separate from UI (Presentational)
- `Cart.jsx` can be used elsewhere with different data.
- Can test the presentational component independently.

- Container component: Handles state and business logic
- Presentational Component: Renders UI based on props. 

Creating the Presentational Component (`cart.jsx`)
- Receives cart items, total price, and handlers via props.
- Renders a simple cart UI.

```js cart.js
const Cart = ({ items, total, onRemove }) => (
  <div>
    <h2>Shopping Cart</h2>
    {items.length === 0 ? <p>Cart is empty</p> : (
      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name} - ${item.price}
            <button onClick={() => onRemove(item.id)}>Remove</button>
          </li>
        ))}
      </ul>
    )}
    <h3>Total: ${total}</h3>
  </div>
);

export default Cart;
```

### Creating the container component
- Manages state for cart items.
- Implements logic to remove items and calculate total.
- Passes data and function to `Cart.jsx`.

```jsx cartContainer.jsx
import { useState } from "react";
import Cart from "./Cart";

const CartContainer = () => {
  const [cart, setCart] = useState([
    { id: 1, name: "React Book", price: 30 },
    { id: 2, name: "JavaScript Guide", price: 25 }
  ]);

  const removeItem = (id) => {
    setCart(cart.filter(item => item.id !== id));
  };

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  return <Cart items={cart} total={total} onRemove={removeItem} />;
};

export default CartContainer;
```