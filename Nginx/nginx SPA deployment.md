routes aren't handled by Nginx. They're handled in the browser using JavaScript.

- `/dashboard`
- `/profile/settings`
> [!INFO]
> These aren't actual files in your server's directory tree! They're virtual routes that your client-side framework is responsible for rendering with the same `index.html`.

> [!WARNING]
> if Nginx gets a request at `/dashboard`.  It won't find `/dashboard` files or folder. 404 for you.

> [!NOTE]
> On an SPA with client-side routing, all unknown paths should fall back to `index.html` so that the JS router can take control.

```nginx
server {
    listen 80;
    server_name mysite.com;

    root /usr/share/nginx/html;

    index index.html;

    location / {
        try_files $uri /index.html;
    }
}
```
