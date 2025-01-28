## How to track user has come from certain path sequence?
To determine if a user has navigated to a React component from a certain path, you can utilize **React Router's `useLocation` and `useNavigationType` hooks** or custom logic. Here's how to do it:

### 1. **Using `useLocation`**

The `useLocation` hook provides information about the current URL, including the `state` object. You can pass state while navigating and check its value in the target component.

#### Example:

```jsx
import { useLocation } from "react-router-dom";

function TargetComponent() {
  const location = useLocation();

  // Check the state or pathname
  if (location.state?.from === "/source-path") {
    console.log("Navigated from /source-path");
  }

  return <div>Target Component</div>;
}

// Navigating with state
import { Link } from "react-router-dom";

function SourceComponent() {
  return (
    <Link to="/target" state={{ from: "/source-path" }}>
      Go to Target
    </Link>
  );
}
```

### 2. **Using `useNavigationType`**

The `useNavigationType` hook helps identify how the navigation occurred (`PUSH`, `REPLACE`, or `POP`).

#### Example:

```jsx
import { useNavigationType } from "react-router-dom";

function TargetComponent() {
  const navigationType = useNavigationType();

  console.log(`Navigation type: ${navigationType}`);
  // Analyze behavior based on `navigationType`
  return <div>Target Component</div>;
}
```

### 3. **Custom Middleware or Context**

If you need to track paths globally, you can set up a context or middleware to store the previous path and access it in your component.

#### Example:

```jsx
import { createContext, useContext, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

const PathContext = createContext();

export function PathProvider({ children }) {
  const location = useLocation();
  const [prevPath, setPrevPath] = useState(null);

  useEffect(() => {
    setPrevPath(location.pathname);
  }, [location]);

  return (
    <PathContext.Provider value={prevPath}>{children}</PathContext.Provider>
  );
}

export function usePrevPath() {
  return useContext(PathContext);
}

// Accessing in a component
function TargetComponent() {
  const prevPath = usePrevPath();
  console.log(`Previous path: ${prevPath}`);
  return <div>Target Component</div>;
}
```

### Summary:

- **`useLocation`:** Pass and check `state` to identify the source.
- **`useNavigationType`:** Identify how navigation occurred.
- **Custom Context:** Track and manage navigation paths globally.

#### Suggestions:

- Use `state` for specific component-to-component communication.
- Use a context for global, reusable path tracking.
- Avoid hardcoding paths; use constants for maintainability.