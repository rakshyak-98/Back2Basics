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
