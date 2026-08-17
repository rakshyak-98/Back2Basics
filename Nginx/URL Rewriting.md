[[nginx URL rewrite]] [[nginx SPA deployment]] [[How does directive work]] [[web server]]

# URL Rewriting

> Map a pretty public URL to a different internal path or entry point — so deep links and refreshes work when there is no real file per route.

```txt
        URL Rewriting ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Product/platform reviews ask why SPAs and frameworks need rewrite/fallback…

## Sources
- [Wikipedia — Rewrite engine](https://en.wikipedia.org/wiki/Rewrite_engine) — overview
- [nginx.org — ngx_http_rewrite_module](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html) — deep-dive
- [Apache — mod_rewrite](https://httpd.apache.org/docs/current/mod/mod_rewrite.html) — overview

## Key Concepts
- **Pretty URL → entry point:** Many frameworks route `/users/1` to `index.html` or `index.php`, not `/users/…
- **Client vs server routing:** SPAs need server fallback for history-mode deep links
- **Rewrite vs redirect:** Internal rewrite keeps the browser URL (often)


- **Core:** URL rewriting transforms a user-facing URL into another internal URL (or entr…

## Technical Details
```nginx
location /legacy/ {
    return 301 /new$request_uri;
}
```

- Nginx-specific rewrite patterns: [[nginx URL rewrite]].
- SPA filesystem fallback: [[nginx SPA deployment]].

| Symptom | Check | Fix |
|---------|-------|-----|
| Old URLs still hit application | rewrite order; location precedence | More specific `location` wins; check `^~` prefix |
| Case-sensitive mismatch | `rewrite` is case-sensitive | Normalize with `map`/`lower` or explicit rules |

## Mistakes to Avoid
- **Mistake:** Chaining more than a few rewrites
- **Mistake:** Confusing cached 301s with internal rewrites
- **Mistake:** Skipping `curl -I` tests when adding rules

## Pros/Cons or Trade-offs
- **Pro:** Stable public URLs while internal structure changes.
- **Con:** Long rewrite chains are hard to debug — keep rules few and documented.

## Comparison
- vs [[nginx URL rewrite]]: concept across servers vs Nginx directives/flags.
- vs application routers: complex rules often belong in the app


### Use cases
- Legacy path redirects after a site migration
