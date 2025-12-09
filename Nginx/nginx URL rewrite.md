
|Nginx directive|What it actually does|When your browser URL becomes|Real folder on disk|
|---|---|---|---|
|`root /var/www/html;`|Physical folder|unchanged|`/var/www/html/blog/post1.html`|
|`alias`|Replace entire path|unchanged|something else|
|`try_files`|“Look here, then here, then fallback”|unchanged|multiple places|
|`rewrite`|**Changes the URL inside Nginx before it looks for files**|can change|depends|
|`return` / `proxy_pass`|Final answer|can change|doesn’t matter|

## Client side routers

> [!INFO]
> most of the time you only need `try_files`
> `rewrite` is only for 'I really want to change the visible URL'

```nginx
location / {
    root /var/www/myapp;           # → looks in /var/www/myapp
    try_files $uri $uri/ /index.html;   # ← THIS IS THE ONLY LINE YOU NEED
}
```

```nginx
location / {
    root /var/www/site;
    try_files $uri $uri.html $uri/ =404;
}
```

What happens when user goes to `/about`

1. Nginx looks for `/var/www/myapp/about` → not found
2. Looks for `/var/www/myapp/about/` → not found
3. Falls back to `/index.html` → React Router handles /about

> [!NOTE]
> Nginx says: “I don’t have a file for this URL → here’s index.html instead. Now it’s your JavaScript’s job to figure out what to show.”

```text
Browser requests → /about
                     ↓
                Nginx on the server
                     ↓
1. Does the file /var/www/myapp/about          exist? → No
2. Does the folder /var/www/myapp/about/       exist? → No
3. Okay, serve /index.html instead (because of try_files)
                     ↓
   → Nginx sends the exact same index.html file that you get on the homepage
                     ↓
   Browser receives index.html and executes your React/Vite app
                     ↓
   React app boots up → React Router (or Vue Router, etc.) looks at the URL bar
                     ↓
   URL bar still says /about → React Router renders the <About /> component
```

> [!INFO]
> That’s it. The magic is that the browser URL never changes — only the file Nginx serves changes.

> ## Why this works perfectly for SPAs (Single Page Applications)
>  - All routes (/, /about, /dashboard, /users/123) → same index.html

> ## What happens if you FORGET this line
>  - User types yoursite.com/about → Nginx looks for file /about → 404 Not Found Even though your React app could handle it perfectly!

## Force remove `.php` or `.html` (hide extension completely)

```nginx
rewrite ^/([^.]+)$ /$1.html last;
```

> [!NOTE]
> Redirect old URL to new ones (SEO critical)

```nginx
# Permanent redirect (301) – Google loves this
rewrite ^/blog/my-old-post.php$ /blog/my-new-post permanent;

# Or with regex capture
rewrite ^/old-path/(.*)$ /new-path/$1 permanent;
```

### Force HTTPS + remove www

```nginx
server {
    listen 80;
    server_name www.example.com example.com;
    return 301 https://example.com$request_uri;
}

server {
    listen 443 ssl;
    server_name www.example.com;
    return 301 https://example.com$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com;
    # your real config here
}
```

```nginx
if ($host ~* ^www\.) forces https and removes www
if ($host ~* ^www\.(.*)$) {
    return 301 https://$1$request_uri;
}
if ($scheme = http) {
    return 301 https://$host$request_uri;
}
```

## "refresh adds a trailing slash and 404s" bug.

### What’s actually happening (step-by-step)

1. You are on: https://yoursite.com/dashboard
2. You click a React Router link → works perfectly (client-side)
3. You press **F5 (refresh)** → browser sends request to server: GET /dashboard
4. Nginx receives /dashboard → looks for a real folder/file
5. Nginx sees there is a folder called dashboard/ in your dist/? → **No** (there isn’t!)
6. But Nginx **automatically tries /dashboard/** (with trailing slash) because many servers treat /dashboard as a directory
7. Nginx now returns **404** (or sometimes serves nothing)