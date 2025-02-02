# How to track user has come from certain path sequence?
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

## In next JS
Tracking **two-step-back navigation** requires maintaining a history of previously visited paths because neither React Router nor Next.js directly provides this functionality. Here's how you can achieve it in **Next.js**:

---

### Approach: Track Navigation History

1. **Use a Global Context for History**
    - Maintain a navigation history in a global context or state.
    - Update the history on every route change.
    - Check the last two paths when needed.

---

#### Example:

```jsx
// context/NavigationContext.js
import { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

const NavigationContext = createContext();

export function NavigationProvider({ children }) {
  const [history, setHistory] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url) => {
      setHistory((prev) => [...prev.slice(-1), url]); // Keep last 2 paths
    };

    router.events.on('routeChangeComplete', handleRouteChange);
    return () => router.events.off('routeChangeComplete', handleRouteChange);
  }, [router]);

  return (
    <NavigationContext.Provider value={{ history }}>
      {children}
    </NavigationContext.Provider>
  );
}

export function useNavigationHistory() {
  return useContext(NavigationContext);
}

// _app.js
import { NavigationProvider } from '../context/NavigationContext';

export default function MyApp({ Component, pageProps }) {
  return (
    <NavigationProvider>
      <Component {...pageProps} />
    </NavigationProvider>
  );
}

// pages/target.js
import { useNavigationHistory } from '../context/NavigationContext';

export default function TargetPage() {
  const { history } = useNavigationHistory();

  if (history.length >= 2 && history[0] === '/classes' && history[1] === '/account') {
    console.log('User visited /classes, then /account, before this page.');
  }

  return <div>Target Page</div>;
}
```

---

### Key Points:

1. **Global Context:** Tracks navigation paths in an array.
2. **`routeChangeComplete` Event:** Captures route changes dynamically.
3. **Condition Check:** Ensures `/classes` → `/account` → Target sequence is matched.

---

### Alternative: Middleware Tracking

If you want server-side logic to handle this:

1. **Store Navigation in Cookies/Session:**
    - Update user’s navigation history in cookies or session on each request.
    - Read and validate history in the middleware or API routes.

#### Example:

```javascript
// middleware.js
import { NextResponse } from 'next/server';

export function middleware(req) {
  const prevHistory = req.cookies.get('nav-history')?.value || [];
  const newPath = req.nextUrl.pathname;

  // Add current path to history
  const updatedHistory = [...prevHistory.split(','), newPath].slice(-3);
  const response = NextResponse.next();
  response.cookies.set('nav-history', updatedHistory.join(','));

  // Check if history matches
  if (updatedHistory[0] === '/classes' && updatedHistory[1] === '/account') {
    console.log('Matched navigation sequence: /classes → /account → current');
  }

  return response;
}
```

---

### Summary:

- **Frontend Context:** Best for client-side checks, real-time tracking.
- **Middleware with Cookies:** Centralized, works for server-side logic.
- **Alternative Options:** Store history in `localStorage` or use analytics libraries.

#### Suggestions:

- Use the **context approach** for simplicity if client-side validation suffices.
- Use **middleware** for server-side validation or centralized navigation tracking.