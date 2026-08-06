[[NextJS]]

# Next js Build

> One-line: what / why for **Next js Build** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Generate Static files]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

> [!WARNING]
> The next js build process, when converting to static files, bakes in environment variables, meaning it cannot read `process.env` at runtime.
- the compiler literally replaces the text `process.env.API_URL` with the actual string value
- When you run a Node.js server, the environment variables live in the server's RAM. When you serve static files via Nginx, the code is running in the **user's browser RAM**. Since the user's browser has no access to your server's terminal or PM2 variables.

## Standard config / commands

…

## Generate Static files

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
	output: "export",
  poweredByHeader: false,
  images: {
    // domains: ["theoterra.com"],
    remotePatterns: [
      {
        hostname: "theoterra.com",
        pathname: "**"
      }
    ]
  }
};

module.exports = nextConfig;

```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
