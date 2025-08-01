If your frontend application is hosted on `https://myapp.com` and it tries to make a request to a backend server (e.g., `https://api.example.com`)

> [!INFO] Yes, it is **possible and common** to use the same origin for both the frontend and backend, especially during local development or when deploying a full-stack application together (e.g., using a monolithic server setup)
- This avoids **CORS issues** altogether because **same-origin requests** are not subject to CORS restrictions.

- **Single-Page Applications (SPAs)** often serve the frontend and API from the same origin using a server like **Express**, **Django**, or **Rails**, which handles both static files (HTML, JS, CSS) and API requests.