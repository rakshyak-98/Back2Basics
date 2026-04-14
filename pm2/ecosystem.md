You create configuration file that PM2 reads when it starts your app.

```js
module.exports = {
  apps: [{
    name: "booking-engine",
    script: "npm start", // or your entry point
    env: {
      // These are injected at runtime
      API_URL: "https://api.example.com",
      NODE_ENV: "production"
    }
  }]
};
```