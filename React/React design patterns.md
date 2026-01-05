## Provider Pattern

```jsx
const ThemeContext = createContext('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}
```

## Presentational Pattern

## Container Pattern

## Controlled Components

## UnControlled Components

## Compound Component

```jsx
import { createContext, useContext, useState } from 'react';

const TabsContext = createContext();

function Tabs({ children, defaultValue }) {
  const [active, setActive] = useState(defaultValue);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      <div>{children}</div>
    </TabsContext.Provider>
  );
}

function Tab({ value, children }) {
  const { active, setActive } = useContext(TabsContext);
  return (
    <button onClick={() => setActive(value)} style={{ fontWeight: active === value ? 'bold' : 'normal' }}>
      {children}
    </button>
  );
}

function TabPanel({ value, children }) {
  const { active } = useContext(TabsContext);
  if (active !== value) return null;
  return <div>{children}</div>;
}

// Usage
<Tabs defaultValue="one">
  <Tab value="one">One</Tab>
  <Tab value="two">Two</Tab>
  <TabPanel value="one">Panel One</TabPanel>
  <TabPanel value="two">Panel Two</TabPanel>
	</Tabs>
```

## Render Props pattern (Data Fetcher API aware components)

## Headless Components

## Context for Global state

## Higher Order components (HOC)

- A function that takes a component and returns an enhanced version. Less common now due to hooks, but still useful for legacy code or cross-cutting concerns.

```tsx
function withAuth<WCP>(WrappedComponent: React.ComponentType<WCP>) {
  return function Enhanced(props: WCP) {
    const isLoggedIn = useAuth(); // custom hook
    return isLoggedIn ? <WrappedComponent {...props} /> : <Redirect to="/login" />;
  };
}

const ProtectedDashboard = withAuth(Dashboard);
```

## Error Boundaries

Yes, I know a lot about React design patterns! They're essential for writing clean, maintainable, scaleable, and performant React code.

Here are some of the most popular and useful **React design patterns** (all in plain JavaScript, as you prefer):

These patterns help solve common problems like:
- Reusability
- Separation of concerns
- State management
- Performance

### 1. **Container and Presentational Components** (Smart vs Dumb)
Separate logic/fetching (container) from UI rendering (presentational).

```jsx
// Container (handles data/logic)
function UserListContainer() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      });
  }, []);

  return <UserList users={users} loading={loading} />;
}

// Presentational (only renders UI)
function UserList({ users, loading }) {
  if (loading) return <p>Loading...</p>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### 2. **Compound Components**
Components that work together and share implicit state (like `<Select><Option /></Select>`).

```jsx
function Toggle() {
  const [on, setOn] = useState(false);
  const toggle = () => setOn(!on);

  return (
    <ToggleContext.Provider value={{ on, toggle }}>
      <div>
        <Toggle.On>The button is on</Toggle.On>
        <Toggle.Off>The button is off</Toggle.Off>
        <Toggle.Button />
      </div>
    </ToggleContext.Provider>
  );
}

const ToggleContext = createContext();

Toggle.On = function On({ children }) {
  const { on } = useContext(ToggleContext);
  return on ? children : null;
};

Toggle.Off = function Off({ children }) {
  const { on } = useContext(ToggleContext);
  return on ? null : children;
};

Toggle.Button = function Button() {
  const { on, toggle } = useContext(ToggleContext);
  return (
    <button onClick={toggle}>
      {on ? 'On' : 'Off'}
    </button>
  );
};
```

### 3. **Custom Hooks Pattern**
Extract logic into reusable hooks (your favourite!).

```jsx
// Custom hook
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}

// Usage
function UserProfile() {
  const { data: user, loading } = useFetch('https://api.example.com/user');

  if (loading) return <p>Loading...</p>;
  return <div>Hello {user.name}</div>;
}
```

### 4. **Render Props Pattern**
Pass a function as a prop to share code.

```jsx
function MouseTracker({ render }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMove = (e) => setPosition({ x: e.clientX, y: e.clientY });
    document.addEventListener('mousemove', handleMove);
    return () => document.removeEventListener('mousemove', handleMove);
  }, []);

  return render(position);
}

// Usage
<MouseTracker render={({ x, y }) => (
  <h1>The mouse is at: {x}, {y}</h1>
)} />
```

### 5. **Higher-Order Components (HOC)**
Function that takes a component and returns an enhanced one.

```jsx
function withLoading(WrappedComponent) {
  return function EnhancedComponent({ isLoading, ...props }) {
    if (isLoading) return <div>Loading...</div>;
    return <WrappedComponent {...props} />;
  };
}

const UserList = ({ users }) => (
  <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
);

const UserListWithLoading = withLoading(UserList);

// Usage
<UserListWithLoading isLoading={loading} users={users} />
```

### 6. **Controlled vs Uncontrolled Components**
Prefer controlled when you need full control over form state.

```jsx
function ControlledForm() {
  const [value, setValue] = useState('');

  return (
    <input
      value={value}
      onChange={(e) => setValue(e.target.value)}
    />
  );
}
```

### 7. **Layout Components**
Extract repeated layout structure.

```jsx
function Card({ title, children }) {
  return (
    <div style={{ border: '1px solid #ccc', borderRadius: 8, padding: 16 }}>
      <h3>{title}</h3>
      {children}
    </div>
  );
}

// Reuse everywhere
<Card title="Profile">
  <p>User info here</p>
</Card>
```


## Props gatter pattern

```jsx
import { useState } from 'react';

function useToggle() {
  const [on, setOn] = useState(false);
  const toggle = () => setOn(!on);

  // Prop getter for the toggler element
  const getTogglerProps = ({ onClick, ...props } = {}) => ({
    'aria-pressed': on,
    onClick: (e: React.MouseEvent) => {
      onClick?.(e);  // Call user's handler first
      toggle();
    },
    ...props,
  });

  return { on, getTogglerProps };
}

// Usage in a render prop or compound component
function Toggle({ children }: { children: (utils: ReturnType<typeof useToggle>) => JSX.Element }) {
  const utils = useToggle();
  return children(utils);
}

// Example usage
function App() {
  return (
    <Toggle>
      {({ on, getTogglerProps }) => (
        <div>
          <button {...getTogglerProps({ 'aria-label': 'custom toggle' })}>
            {on ? 'On' : 'Off'}
          </button>
          {/* User can add their own onClick without breaking toggle */}
          <div {...getTogglerProps({ onClick: () => console.log('Extra!') })}>
            Clickable Div (also toggles)
          </div>
        </div>
      )}
    </Toggle>
  );
}
```

## Component Pattern to handle Network request

> [!INFO]
> For production: Use TanStack Query + Suspense/Error Boundaries — it handles 90% of edge cases (stale-while-revalidate, refetch on focus, etc.).

- The preferred modern approach. Encapsulate fetching logic (using fetch, Axios, etc.) in a reusable hook with `useState` and `useEffect`.

- Container/Presentational (Smart/Dumb) Components
	- Container (smart) -> Handles data fetching, state management, and business logic.
	- Presentational (dumb) -> Pure UI rendering based on props (no fetching).

- Higher-Order Components (HOC)
> [!INFO]
> - A function that takes a component and returns an enhanced version (e.g., `withDataFetching(WrappedComponent)`). Add fetching logic, loading indicator, or error handling without modifying the original component.
> - Example: `withLoader` HOC fetches data and shows "Loading..." until ready.