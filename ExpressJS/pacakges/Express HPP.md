- HPP (HTTP Parameter Pollution)
is an attack technique where an attacker injects multiple parameters with the same name in an HTTP request to manipulate backed logic.

```txt
GET /api/user?id=123&id=456
```

`hpp` is a middleware in Express JS that prevents HTTP Parameter Pollution by allowing only the first occurrence of a parameter in a request.

```js
import express from "express";
import hpp from "hpp";

const app = express();

// Apply HPP middleware
app.use(hpp());

app.get("/api/user", (req, res) => {
  res.send(`User ID: ${req.query.id}`);
});

app.listen(3000, () => console.log("Server running on port 3000"));

```