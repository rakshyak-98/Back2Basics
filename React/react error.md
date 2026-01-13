
```text
X-Content-Type-Options: nosniff

```

`X-Content-Type-Options` -> "Hey browser trust the file type I told you (like `.js` or `.css`) Don't try to be smart and guess different type."

Some hackers uploaded a file that looks like an image but is actually malicious code. The browser might "sniff" it and think "oh this is actually JavaScript" and run the bad code.

---

```text
Uncaught Error: Rendered fewer hooks than expected. This may be caused by an accidental early return statement.
```

> [!INFO]
> - means that the number of hooks called changed between renders — and in 99% of cases, the reason is an early return before all hooks have been called.

```jsx
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const user = null;
  const [data, setData] = useState();

  if (!user) {
    return;
  }

  const [data2, setData2] = useState();

  useEffect(() => {
    if (!user) {
      return;
    }
  }, []);
  return (
    <div>
      <h1>Hello wrold</h1>
    </div>
  );
}

export default App;

```

```jsx
function App() {
  const user = null;
  const [data, setData] = useState();          // Hook 1

  if (!user) {
    return;                                 // ← Early return!
  }

  const [data2, setData2] = useState();       // Hook 2 — sometimes reached, sometimes not
  useEffect(() => { ... }, []);               // Hook 3 — sometimes reached, sometimes not

  return <div>...</div>;
}
```