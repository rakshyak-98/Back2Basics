> [!INFO] NextJS build will call api 
[next-router-not-mounted](https://nextjs.org/docs/messages/next-router-not-mounted)
error comes from `Next.js v13+` App Router
- If used in the `app` directory, migrate to the new hooks imported from `next/navigation`.
use new `next/navigation` hooks
```js
import { useRouter, useSearchParams, useParams } from 'next/navigation'
```

 Why the changes?
App Router runs in a **React Server Component-first architecture**. The old hooks from `next/router` depend on the client-side routing context — which doesn't exist in server components.

The new `next/navigation` hooks are **designed to work with [[RSC (React Server Component boundaries)]] and match the new routing paradigm.

```text
Module not found: Can't resolve '@/app/store/store.js'
```

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}

```

```text
this error : TypeError: (0 , {imported module [project]/nodemodules/next/dist/server/route-modules/app-page/vendored/rsc/react.js [app-rsc] (ecmascript)}.useContext) is not a function
```

- you're importing a vendored/interval version of React from `Next.js` RSC (`react.js [app-rsc]`) instead of the public React module.

## Pre-render Error with NextJS
```txt
Error occured prerendering path /menu-items.
```
[NextJS prerender-error](https://nextjs.org/docs/messages/prerender-error)

> [!NOTE] app route -> app router allow colocation of pages and other files in the same folder.

- [avoid exporting pages with server-side rendering](https://nextjs.org/docs/messages/prerender-error#4-avoid-exporting-pages-with-server-side-rendering) -> If you're using `next export` or `output: 'export'` in your `next.config.js`, ensure that none of your pages use `getServerSideProps`. Instead, use `getStaticProps` for data fetching:

### Next JS export to static HTML always redirect to the home page "/" if page refresh
[discussion vercel nextjs](https://github.com/vercel/next.js/discussions/10522)
[discussioncomment-2304314](https://github.com/vercel/next.js/discussions/10522#discussioncomment-2304314)


# Process already running
```bash
npm run start;
pkill -3 npm;
```

```text
> dinehub@0.1.0 start
> next start

 ⨯ Failed to start server
Error: listen EADDRINUSE: address already in use :::3000
    at <unknown> (Error: listen EADDRINUSE: address already in use :::3000)
    at new Promise (<anonymous>) {
  code: 'EADDRINUSE',
  errno: -98,
  syscall: 'listen',
  address: '::',
  port: 3000
}

```

```txt

> dinehub@0.1.0 start
> next start

   ▲ Next.js 15.2.4
   - Local:        http://localhost:3000
   - Network:      http://192.168.29.101:3000

 ✓ Starting...
 ✓ Ready in 1812ms
Quit (core dumped)

```

```bash
ps aux | grep next;
```


> [!NOTE] check the start time before killing (not accedentaly killing another process)
```txt
rakshyak   18329  0.0  0.0   2896  1536 pts/0    S    12:16   0:00 sh -c next start
rakshyak   18330  4.8  1.2 14404692 146420 pts/0 Sl   12:16   0:04 next-server (v15.2.4)

```

```bash
pkill next-server;
```

### Fix CORS error
- use inbuild `app/api` routes to call external APIs.

## Static image not loading when hosted on AWS ec2 instance

### Nginx proxy setup error, not able to call API

### NextJS build error
```txt
Error: ENOENT: no such file or directory, open '$PWD/.next/prerender-manifest.json'
```
- `.next/prerender-manifest.json` is an internal build artifact generated during `next build`. it contains metadata used by the server to efficiently serve statically pre-rendered pages (SSG) and handle ISR (Incremental Static Regeneration).
- SSR server uses this to determine, if a route is static or needs regeneration, where to load the pre-rendered HTML/JSON.
- `.rsc` extension inside `.next` are compiled artifacts of server components used for server-side streaming and rendering. Generated during `next build` or `next dev`.

> [!INFO]
> `.rsc` files are not editable or human-readable they're used internally for optimised React rendering.
> on request `.rsc` is streamed to client or edge, allowing partial hydration.

| File    | Purpose                                |
| ------- | -------------------------------------- |
| `.rsc`  | Compiled React Server Component output |
| `.js`   | Client-side JS bundle                  |
| `.html` | Static HTML fallback or initial render |


### useSearchParams() should be wrapped in a suspense boundary at page "/reserve-table". Read more: https://nextjs.org/docs/messages/missing-suspense-with-csr-bailout
- `useSearchParams` is a client Component only hook from `next/navigation`, and you're using it outside a proper Suspense boundary in new Next.js App router.
- solution -> wrap the part of your component that uses `useSearchParams()` in a `<Suspense>` block to allow Next.js handle the client side Rendering (CSR) bailout gracefully.
```js
// app/reserve-table/page.tsx

import { Suspense } from "react";
import ReserveTableContent from "./ReserveTableContent";

export default function ReserveTablePage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ReserveTableContent />
    </Suspense>
  );
}

```
- `useSearchParams()` needs client-side runtime.
- App Router does SSR/Streaming by default. It needs a suspense boundary to isolate client components that rely on the browser environment.


## `Collecting page data  ...TypeError: Super expression must either be null or a function, not undefined`

- due to `use client` directive not mentioned in component.