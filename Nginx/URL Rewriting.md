[[Nginx]]

# URL Rewriting

> URL Rewriting — a technique used by web servers (like Apache, Nginx, IIS, etc.) or web frameworks to transform a "pretty" or user-friendly URL into a…

---

## How it works

URL rewriting is a technique used by web servers (like Apache, Nginx, IIS, etc.) or web frameworks to **transform a "pretty" or user-friendly URL into a different internal URL** that the server actually uses to locate and serve the correct file, script, or content.
### Why is it used?
Most modern web applications (especially single-page applications or framework-based sites like React, Angular, Vue, Laravel, Next.js, etc.)
- do **not** have real physical files or folders for every URL path. Instead, they use **client-side routing** or **server-side routing** that points many (or all) URLs to a single entry point (e.g., index.html or application.php).
To make this work without breaking when users refresh the page or visit a deep link directly, the server uses **URL rewriting** to redirect all requests (or specific patterns) to that single entry point.


## Configuration and commands

```nginx
location /legacy/ {
    return 301 /new$request_uri;
}
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Old URLs still hit application | rewrite order; location precedence | More specific `location` wins; check `^~` prefix |
| Case-sensitive mismatch | `rewrite` is case-sensitive | Normalize with `lower` map or explicit rules |

---


## Gotchas

> [!WARNING]
> Long rewrite chains are hard to debug — document each rule and test with `curl -I`.

---


## When not to use

- Do not chain more than a few rewrites — use application routing for complex rules.


---


## Related

[[Nginx]]

## Sources

- [Wikipedia — URL Rewriting](https://en.wikipedia.org/wiki/URL_Rewriting)
