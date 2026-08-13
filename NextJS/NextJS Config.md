[[NextJS]] [[Next JS]] [[typescript]]

# NextJS Config

> `next.config.js` — Next.js knobs: redirects, headers, images, transpile packages, experimental flags.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** One configuration file shapes build + runtime behavior. Prefer documented options over undocumented experimental flags in production.

```txt
next.config.* ──build/runtime──► output + routing behavior
```

---

## Standard config / commands

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: { remotePatterns: [{ protocol: 'https', hostname: 'cdn.example.com' }] },
  async headers() {
    return [{ source: '/(.*)', headers: [{ key: 'X-Frame-Options', value: 'DENY' }] }]
  },
}
module.exports = nextConfig
```

| Knob | Why it matters |
|------|----------------|
| `output: 'standalone'` | Docker-friendly |
| `basePath`/`assetPrefix` | Subpath deploys |
| `transpilePackages` | Monorepo libs |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Image host refused | `images.remotePatterns` | Allow hostname |
| Wrong asset URLs | basePath | Align CDN/prefix |
| ESM/CJS config load | File type | `.mjs` / `next.config.ts` care |
| Headers not applied | Source pattern | Fix matchers |

---

## Gotchas

> [!WARNING]
> **Restart required** for many config changes.

> [!WARNING]
> **Experimental flags** — churn between majors.

---

## When NOT to use

- **application logic** — keep out of configuration; use code.
- **Secrets** — environment, not configuration committed.

---

## Related

[[Next JS]] [[Next js Build]] [[HTTP Strict Transport Security]]
