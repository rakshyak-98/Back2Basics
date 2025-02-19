Instead of passing multiple props, the parent component manages the state, and child components communicate implicitly.

### How it works
We break the component into self-contained components

```js Cart.jsx
import { createContext, useContext, useState } from "react";

const CartContext = createContext();

const Cart = ({ children }) => {
  const [items, setItems] = useState([
    { id: 1, name: "React Book", price: 30 },
    { id: 2, name: "JavaScript Guide", price: 25 }
  ]);

  const removeItem = (id) => {
    setItems(items.filter(item => item.id !== id));
  };

  const total = items.reduce((sum, item) => sum + item.price, 0);

  return (
    <CartContext.Provider value={{ items, removeItem, total }}>
      <div>
        <h2>Shopping Cart</h2>
        {children}
      </div>
    </CartContext.Provider>
  );
};
```

```js Cart.Item.jsx
Cart.Item = ({ item }) => {
  return (
    <div>
      {item.name} - ${item.price}
      <Cart.RemoveButton id={item.id} />
    </div>
  );
};
```

```js Cart.Total.jsx
Cart.Total = () => {
  const { total } = useContext(CartContext);
  return <h3>Total: ${total}</h3>;
};
```

```js Cart.RemoveButton.jsx
Cart.RemoveButton = ({ id }) => {
  const { removeItem } = useContext(CartContext);
  return <button onClick={() => removeItem(id)}>Remove</button>;
};
```

## Implementation of a Tabs component
- It allows consumers to define `TabList`, Tab and `TabPanel` without explicit prop drilling.
- The Tabs parent manages active state and exposes subcomponents.

Tabs (Parent): Manages active state.
Tabs.List: Holds multiple `Tab` elements.
Tabs.Tab: Represents an individual tab button.
Tabs.panel: Displays the content of the active tab.

```js Tabs.jsx
import { createContext, useContext, useState } from "react";

const TabsContext = createContext();

const Tabs = ({ children }) => {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div>{children}</div>
    </TabsContext.Provider>
  );
};
```

```js Tab.List
Tabs.List = ({ children }) => <div>{children}</div>;
```

```js Tabs.Tab
Tabs.Tab = ({ index, children }) => {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  
  return (
    <button 
      onClick={() => setActiveTab(index)}
      style={{ fontWeight: activeTab === index ? "bold" : "normal" }}
    >
      {children}
    </button>
  );
};
```

```js Tabs.Panel.jsx
Tabs.Panel = ({ index, children }) => {
  const { activeTab } = useContext(TabsContext);
  
  return activeTab === index ? <div>{children}</div> : null;
};
```

```js App.jsx
import Tabs from "./Tabs";

const App = () => (
  <Tabs>
    <Tabs.List>
      <Tabs.Tab index={0}>Tab 1</Tabs.Tab>
      <Tabs.Tab index={1}>Tab 2</Tabs.Tab>
      <Tabs.Tab index={2}>Tab 3</Tabs.Tab>
    </Tabs.List>

    <Tabs.Panel index={0}>Content for Tab 1</Tabs.Panel>
    <Tabs.Panel index={1}>Content for Tab 2</Tabs.Panel>
    <Tabs.Panel index={2}>Content for Tab 3</Tabs.Panel>
  </Tabs>
);

export default App;
```