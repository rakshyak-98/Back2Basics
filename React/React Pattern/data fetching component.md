## `useEffect` (Classic Client-Side Fetching)

```jsx
import { useState, useEffect } from 'react';

function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://api.example.com/user')
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;
  return <div>{user?.name}</div>;
}
```

## React Suspense with use Hook

```jsx
import { use } from 'react';
import { Suspense } from 'react';

async function fetchUser() {
  const res = await fetch('https://api.example.com/user');
  return res.json();
}

function UserProfile() {
  const user = use(fetchUser()); // Suspends until resolved
  return <div>{user.name}</div>;
}

function App() {
  return (
    <Suspense fallback={<p>Loading user...</p>}>
      <UserProfile />
    </Suspense>
  );
}
```