If your frontend application is hosted on `https://myapp.com` and it tries to make a request to a backend server (e.g., `https://api.example.com`)

> [!INFO] Yes, it is **possible and common** to use the same origin for both the frontend and backend, especially during local development or when deploying a full-stack application together (e.g., using a monolithic server setup)
- This avoids **CORS issues** altogether because **same-origin requests** are not subject to CORS restrictions.

- **Single-Page Applications (SPA)** often serve the frontend and API from the same origin using a server like **Express**, **Django**, or **Rails**, which handles both static files (HTML, JS, CSS) and API requests.


## `withCredentials`
When you enable `withCredentials: true`, the browser treats the request as a credentialed request. According to CORS specification, the server is forbidden from using the wildcard `*` for `Access-Control-Allow-Origin` when credentials are sent. It must echo back your exact origin. 

### CORS middleware in Express (`cors` package)
```js
const corsOptions = {
  origin: ['https://yoursite.com', 'http://localhost:3000'],
  credentials: true
};
app.use(cors(corsOptions));
```

### Client side `axios` config
```js
const api = axios.create({
  baseURL: 'https://api.yourbackend.com',
  withCredentials: true   // this triggers the stricter CORS rules
});
```