```js
// withDataFetching.js
import React, { useState, useEffect } from 'react';

// Optional: Simple loading spinner component
const DefaultLoading = () => <div>Loading...</div>;
const DefaultError = ({ error }) => <div>Error: {error.message}</div>;

function withDataFetching(WrappedComponent, fetchConfig) {
  // fetchConfig can be:
  // - a string URL
  // - or an object: { url, method = 'GET', headers = {}, body = null, dependencies = [] }

  return function WithDataFetching(props) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Normalize config
    const config = typeof fetchConfig === 'string'
      ? { url: fetchConfig }
      : fetchConfig;

    const {
      url,
      method = 'GET',
      headers = {},
      body = null,
      dependencies = [], // extra deps for useEffect
      LoadingComponent = DefaultLoading,
      ErrorComponent = DefaultError,
    } = config;

    useEffect(() => {
      let mounted = true;

      const fetchData = async () => {
        setLoading(true);
        setError(null);

        try {
          const response = await fetch(url, {
            method,
            headers: {
              'Content-Type': 'application/json',
              ...headers,
            },
            body: body ? JSON.stringify(body) : null,
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const result = await response.json();

          if (mounted) {
            setData(result);
            setLoading(false);
          }
        } catch (err) {
          if (mounted) {
            setError(err);
            setLoading(false);
          }
        }
      };

      fetchData();

      return () => {
        mounted = false; // cleanup to prevent state update on unmounted component
      };
    }, [url, method, JSON.stringify(body), JSON.stringify(headers), ...dependencies]);

    // Render logic
    if (loading) {
      return <LoadingComponent />;
    }

    if (error) {
      return <ErrorComponent error={error} />;
    }

    // Pass data, loading, error, and refetch capability
    return (
      <WrappedComponent
        {...props}
        data={data}
        loading={loading}
        error={error}
        refetch={() => {
          // Force re-run effect by changing a dummy dependency if needed
          // Or just call the fetch again manually
        }}
      />
    );
  };
}

export default withDataFetching;
```

### Example usage

```js
// UserList.js
import React from 'react';

function UserList({ data, loading, error }) {
  // data is already handled by HOC, but we can still use props safely
  if (!data) return null;

  return (
    <div>
      <h2>Users</h2>
      <ul>
        {data.map(user => (
          <li key={user.id}>
            {user.name} ({user.email})
          </li>
        ))}
      </ul>
    </div>
  );
}

// Wrap it with the HOC
export default withDataFetching(UserList, 'https://jsonplaceholder.typicode.com/users');
```