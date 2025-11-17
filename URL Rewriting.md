URL rewriting is a technique used by web servers (like Apache, Nginx, IIS, etc.) or web frameworks to **transform a "pretty" or user-friendly URL into a different internal URL** that the server actually uses to locate and serve the correct file, script, or content.

### Why is it used?

Most modern web applications (especially single-page applications or framework-based sites like React, Angular, Vue, Laravel, Next.js, etc.)
- do **not** have real physical files or folders for every URL path. Instead, they use **client-side routing** or **server-side routing** that points many (or all) URLs to a single entry point (e.g., index.html or app.php).

To make this work without breaking when users refresh the page or visit a deep link directly, the server uses **URL rewriting** to redirect all requests (or specific patterns) to that single entry point.