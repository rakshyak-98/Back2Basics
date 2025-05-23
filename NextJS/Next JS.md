> [!INFO] In NextJS, when using `next/router`, the query parameters might be undefined on the first render because NextJS initially renders the page on the server (or statically), and _the query values are only available after hydration on the client.


### Image

```txt
Error: Invalid src prop [(https://picsum.photos/seed/DUeHUGir/1880/2247)](https://picsum.photos/seed/DUeHUGir/1880/2247) on `next/image`, hostname "picsum.photos" is not configured under images in your `next.config.js` See more info: [https://nextjs.org/docs/messages/next-image-unconfigured-host](https://nextjs.org/docs/messages/next-image-unconfigured-host)
```
- NextJS restricts external image resources for `next/image` by default. You need to allow `hostname` in your `next.config.js` file.

#### Allow External images in `next.config.js`
```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "picsum.photos",
      },
    ],
  },
};

module.exports = nextConfig;

```

### Page route
- in NextJS application, any file inside the `pages/` directory become a route.
- To create a directory inside `pages/` that NextJS ignores.

```txt
pages/
  _apiSlice/  <-- Ignored by Next.js routing
  index.js

```

### next Router
`asPath` is a property of `useRouter()` from `next/Router` ant it returns the URL path as seen in the browser (including query parameters but without considering dynamic route patterns)
```ts
import { useRouter } from "next/router";

export default function Page() {
  const router = useRouter();

  return <p>Current Path: {router.asPath}</p>;
}

```

| Property   | Example Route             | Description                                            |
| ---------- | ------------------------- | ------------------------------------------------------ |
| `asPath`   | `/product/10?sort=asc`    | the actual URL in the browser, including query params. |
| `pathName` | `/product/[id]`           | the NextJS route pattern (dynamic route name).         |
| `query`    | `{id: "10", sort: "asc"}` | extracted query parameters as an object.               |
#### Map an incoming request path with `rewrites`
- `rewrites` allow you to map an incoming request path to a different destination path.
- `rewriets` act as a URL prozy and mask the destination path.

> [!NOTE] `rewrites` are applied to client-side routing, a `<Link href="/about">` will have the rewrite.

```js
// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",  // Match any API route
        destination: "https://backend.example.com/api/:path*", // Proxy to backend
      },
    ];
  },
};

```

### Manifest json file

- enables code splitting, lazy loading
- [[SSR]] needs to know which chunks to send.
- Middleware/runtime matches routes and behaviors based on manifest.

> [!INFO] manifest json file
> - allow static hosting/CDNs to understand asset dependencies.

- `*-manifest.json` files serve as internal maps used by the framework and server to efficiently resolve resources.

| File Name                        | Purpose                                                     |
| -------------------------------- | ----------------------------------------------------------- |
| `build-manifest.json`            | Map of all built files for each route/page (JS/CSS chunks)  |
| `react-loadable-manifest.json`   | Helps with dynamic imports & SSR chunk resolution           |
| `ssr-module-manifest.json`       | Used by the server to know which modules to preload for SSR |
| `middleware-manifest.json`       | Metadata for middleware (functions, matchers)               |
| `routes-manifest.json`           | List of all static + dynamic routes and rewrites/redirects  |
| `client-reference-manifest.json` | Tracks server components vs client components for RSC       |
| `app-build-manifest.json`        | Used in App Router builds (maps pages to built files)       |
### Next dynamic
```js
export default dynamic(() => Promise.resolve(Home_1), { ssr: false })
```
> [!INFO] 
> dynamically load the component and do not render this component of ssr.
