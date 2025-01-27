A Class Management component composed of smaller components like `ClassHeader` `ClassBody` and `ClassFooter`.

```ts
import React, { createContext, useContext, useState } from "react";

// Context for managing class data
const ClassContext = createContext();

export const ClassManagement = ({ children }) => {
    const [students, setStudents] = useState([
        { id: 1, name: "Alice" },
        { id: 2, name: "Bob" },
    ]);
    const [isClassActive, setIsClassActive] = useState(false);

    const addStudent = (student) => setStudents((prev) => [...prev, student]);
    const removeStudent = (id) =>
        setStudents((prev) => prev.filter((student) => student.id !== id));
    const toggleClass = () => setIsClassActive((prev) => !prev);

    return (
        <ClassContext.Provider
            value={{
                students,
                isClassActive,
                addStudent,
                removeStudent,
                toggleClass,
            }}
        >
            <div className="class-management">{children}</div>
        </ClassContext.Provider>
    );
};

// Hook for consuming context
export const useClass = () => useContext(ClassContext);

```

```ts
export const ClassHeader = () => {
    const { isClassActive, toggleClass } = useClass();

    return (
        <header className="class-header">
            <h2>Class Status: {isClassActive ? "Active" : "Inactive"}</h2>
            <button onClick={toggleClass}>
                {isClassActive ? "End Class" : "Start Class"}
            </button>
        </header>
    );
};
```

```ts
export const ClassBody = () => {
    const { students, removeStudent } = useClass();

    return (
        <div className="class-body">
            <h3>Students</h3>
            <ul>
                {students.map((student) => (
                    <li key={student.id}>
                        {student.name}{" "}
                        <button onClick={() => removeStudent(student.id)}>
                            Remove
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};
```

```ts
export const ClassHeader = () => {
    const { isClassActive, toggleClass } = useClass();

    return (
        <header className="class-header">
            <h2>Class Status: {isClassActive ? "Active" : "Inactive"}</h2>
            <button onClick={toggleClass}>
                {isClassActive ? "End Class" : "Start Class"}
            </button>
        </header>
    );
};
```

```ts
export const ClassBody = () => {
    const { students, removeStudent } = useClass();

    return (
        <div className="class-body">
            <h3>Students</h3>
            <ul>
                {students.map((student) => (
                    <li key={student.id}>
                        {student.name}{" "}
                        <button onClick={() => removeStudent(student.id)}>
                            Remove
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};
```

```ts
import React from "react";
import { ClassManagement, ClassHeader, ClassBody, ClassFooter } from "./ClassComponents";

const App = () => {
    return (
        <ClassManagement>
            <ClassHeader />
            <ClassBody />
            <ClassFooter />
        </ClassManagement>
    );
};

export default App;


```

## Cart Provider pattern
It's generally not recommended to place routing logic directly in the **Cart Provider** component. The **Cart Provider** should focus on managing the cart's state and actions (like adding/removing items, updating totals, etc.), not routing or navigation.

### **Why it's not ideal:**

1. **Separation of Concerns**:
    
    - The **Cart Provider** is responsible for state management (cart-related data), while routing should be handled separately. Mixing concerns can make your code harder to maintain and test.
2. **Reusability**:
    
    - Keeping routing logic in the provider would make the provider tightly coupled to the routing logic, limiting the ability to reuse the **Cart Provider** component in different routes or contexts.
3. **Testability**:
    
    - It's easier to test the cart functionality if it's decoupled from navigation. Combining both in the same component might make unit testing more complicated.

---

### **Better Approach:**

Instead of putting routing logic in the **Cart Provider**, consider using a **separate component** for navigation after the checkout button is clicked. You can use **React Router** (or **Next.js's `useRouter`**) to handle the routing outside the provider.

---

### **Implementation Example:**

#### **1. CartProvider Component** (Focus on Cart State)

```jsx
import React, { createContext, useContext, useState } from "react";

const CartContext = createContext();

export const CartProvider = ({ children }) => {
    const [cartItems, setCartItems] = useState([]);
    const [totalAmount, setTotalAmount] = useState(0);

    const addToCart = (item) => {
        setCartItems((prev) => [...prev, item]);
        setTotalAmount((prev) => prev + item.price);
    };

    const proceedToCheckout = () => {
        // Logic to proceed (e.g., prepare cart data for checkout)
    };

    return (
        <CartContext.Provider value={{ cartItems, totalAmount, addToCart, proceedToCheckout }}>
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => useContext(CartContext);
```

#### **2. ProceedToCheckout Component** (Handles Routing Logic)

```jsx
import React from "react";
import { useRouter } from "next/router"; // Using Next.js's routing hook
import { useCart } from "./CartProvider";

const ProceedToCheckout = () => {
    const { totalAmount, proceedToCheckout } = useCart();
    const router = useRouter();

    const handleProceed = () => {
        proceedToCheckout(); // Any final preparations (e.g., data verification)
        router.push("/checkout"); // Navigate to the checkout page
    };

    return (
        <div>
            <button onClick={handleProceed}>Proceed to Checkout</button>
            {totalAmount > 0 && <p>Total Amount: {totalAmount}</p>}
        </div>
    );
};

export default ProceedToCheckout;
```

#### **3. Usage in App Component**

```jsx
import { CartProvider } from "./CartProvider";
import ProceedToCheckout from "./ProceedToCheckout";

const App = () => {
    return (
        <CartProvider>
            {/* Other components */}
            <ProceedToCheckout />
        </CartProvider>
    );
};

export default App;
```

---

### **Advantages of This Approach:**

1. **Clean Separation**: Cart logic and routing are handled separately, maintaining the separation of concerns.
2. **Testability**: Both the cart state logic and the routing logic are easier to test independently.
3. **Maintainability**: Routing logic is now isolated, so it’s easier to update or change the routing logic in the future without affecting the cart provider.

---

Let me know if you need further clarification or a deeper dive into any part of this!
