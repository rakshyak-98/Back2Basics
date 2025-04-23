[next-router-not-mounted](https://nextjs.org/docs/messages/next-router-not-mounted)
error comes from `Next.js v13+` App Router
- If used in the `app` directory, migrate to the new hooks imported from `next/navigation`.
use new `next/navigation` hooks
```js
import { useRouter, useSearchParams, useParams } from 'next/navigation'
```

### Why the changes?
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

## Prerender Error with NextJS
```txt
Error occured prerendering path /menu-items.
```
[NextJS prerender-error](https://nextjs.org/docs/messages/prerender-error)

> [!NOTE] app route -> app router allow colocation of pages and other files in the same folder.

- [avoid exporting pages with server-side rendering](https://nextjs.org/docs/messages/prerender-error#4-avoid-exporting-pages-with-server-side-rendering) -> If you're using `next export` or `output: 'export'` in your `next.config.js`, ensure that none of your pages use `getServerSideProps`. Instead, use `getStaticProps` for data fetching:

### Next JS export to static HTML always redirect to the home page "/" if page refresh
[discussion vercel nextjs](https://github.com/vercel/next.js/discussions/10522)
[discussioncomment-2304314](https://github.com/vercel/next.js/discussions/10522#discussioncomment-2304314)
