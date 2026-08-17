[[vercel deployment]] [[Deployment/render cli]] [[Proxy/Reverse Proxy]]

# Netlify deployment

> Git-connected Jamstack host — Netlify runs your build command, publishes the output directory to a CDN, and attaches functions/redirects as configured.





## Interview Relevance
Interviewers compare Netlify vs Vercel: build/publish dirs, `_redirects`/`netlify.toml`, and SPA fallback behavior.

## Sources
- [Netlify docs — Deploy](https://docs.netlify.com/site-deploys/overview/) — deep-dive
- [Netlify — netlify.toml](https://docs.netlify.com/configure-builds/file-based-configuration/) — overview

## Recall Cues
- Why do interviewers care about Interviewers compare Netlify vs Vercel: build/publish dirs, `_redirects`/`netlify.toml`, and SPA fallback behavior?
- What mistake is **Wrong `publish` directory (deploying repo root)**?
- What mistake is **Secrets in client-side environment variables**?
- What mistake is **Forgetting branch deploy vs production context variables**?

## Technical Details
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

```bash
netlify deploy --build
netlify deploy --prod
```

| Concern | Knob |
|---------|------|
| SPA refresh 404 | rewrite to `index.html` |
| Env vars | Site settings / context-specific |
| Headers | `[[headers]]` in toml |

## Mistakes to Avoid
- Wrong `publish` directory (deploying repo root).
- Secrets in client-side environment variables.
- Forgetting branch deploy vs production context variables.

## Comparison
- vs [[vercel deployment]]: similar Jamstack shape; different config files and function models.
- vs classic VM+Nginx: less OS ops; more platform limits.

## Real-World Applications
Marketing sites and Vite/React SPAs with form handling or light functions.

**Example:** Vue Router history mode 404 on refresh — add the SPA rewrite above.

## Pros/Cons or Trade-offs
- **Pro:** Simple static+functions workflow and previews.
- **Con:** Long-lived servers/websockets need another platform.
