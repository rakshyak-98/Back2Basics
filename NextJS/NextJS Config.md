[[Next JS]] [[Next js Build]] [[NextJS Deployment]] [[HTTP Strict Transport Security]]

# NextJS Config

> `next.config.js` (or `.mjs` / `.ts`) holds Next.js knobs — redirects, headers, images, and build output — without putting app logic in the configuration file.

## Interview Relevance

Interviewers ask about `next.config` to see if you know which settings affect deploy shape (`output`, `basePath`), security headers, and image allowlists — and what must live in environment variables instead.

## Sources

- [Next.js Docs — next.config.js Options](https://nextjs.org/docs/app/api-reference/config/next-config-js) — deep-dive
- [Next.js Docs — Configuring](https://nextjs.org/docs/app/api-reference/config) — overview

## Core Definition

`next.config.*` is a Node module loaded at build and server start; it is not shipped to the browser, and it shapes routing, asset URLs, and feature flags for the whole app.

## Key Concepts

- **File forms:** `.js`, `.mjs`, or `.ts` → pick ESM vs CJS carefully; `.cjs`/`.cts` are not supported.
- **`output: 'standalone'`:** traces a minimal Node server tree → friendlier Docker images.
- **`basePath` / `assetPrefix`:** subpath or CDN URLs → wrong values break CSS/JS after deploy.
- **`images.remotePatterns`:** allowlist for `next/image` remotes → refusals are configuration, not magic.
- **`headers` / `redirects` / `rewrites`:** edge routing and security headers → keep secrets out of committed configuration.

## Technical Details

```txt
next.config.* ──build/runtime──► output + routing behavior
```

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  images: {
    remotePatterns: [{ protocol: 'https', hostname: 'cdn.example.com' }],
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [{ key: 'X-Frame-Options', value: 'DENY' }],
      },
    ]
  },
}
module.exports = nextConfig
```

| Knob | Why it matters |
|------|----------------|
| `output: 'standalone'` | Smaller self-hosted / Docker deploys |
| `basePath` / `assetPrefix` | Subpath and CDN asset URLs |
| `transpilePackages` | Monorepo packages that need compiling |
| `typescript.ignoreBuildErrors` | Never enable for production quality |

| Symptom | Check | Fix |
|---------|-------|-----|
| Image host refused | `images.remotePatterns` | Allow the hostname |
| Wrong asset URLs | `basePath` / `assetPrefix` | Align with CDN and host path |
| Configuration load failure | ESM vs CJS | Prefer `next.config.mjs` or `.ts` carefully |
| Headers not applied | `source` matcher | Fix path patterns |

## Real-World Applications

Teams set `standalone` for Kubernetes, pin remote image hosts for a CDN, and add [[HTTP Strict Transport Security]] plus frame-denial headers in one place.

**Example:** App served under `https://example.com/app` needs `basePath: '/app'` or every static asset 404s.

## Pros/Cons or Trade-offs

- **Pro:** Central, typed knobs for deploy and security — reviewers see intent in one file.
- **Con:** Many options require a process restart; experimental flags churn across majors.
- **Con:** Putting business rules in configuration makes testing and reuse harder than code.

## Comparison

- vs environment variables: secrets and per-environment values belong in the environment; configuration holds structure and allowlists.
- vs route handlers / middleware: request-time logic stays in code; configuration sets global defaults.

## Mistakes to Avoid

- Committing secrets in `next.config` — use environment variables.
- Enabling `typescript.ignoreBuildErrors` to “green” CI — ships broken contracts.
- Forgetting that many configuration changes need a restart of `next dev` / rebuild.
