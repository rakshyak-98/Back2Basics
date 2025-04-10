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