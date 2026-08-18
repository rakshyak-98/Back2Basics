[[NextJS]]

# NextJS Error

> NextJS Error — error comes from Next.js v13+ App Router

## Mental model

**Say it in one breath:** NextJS Error — I can explain the job, the configuration, and the top failure without jargon.

> [!INFO] NextJS build will call api
[next-router-not-mounted](https://nextjs.org/docs/messages/next-router-not-mounted)
error comes from `Next.js v13+` application Router
- If used in the `app` directory, migrate to the new hooks imported from `next/navigation`.
use new `next/navigation` hooks
```js
import { useRouter, useSearchParams, useParams } from 'next/navigation'
```
 Why the changes?
application Router runs in a **React Server Component-first architecture**. The old hooks from `next/router` depend on the client-side routing context — which doesn't exist in server components.
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

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **NextJS Error** | This note’s core idea | “I explain NextJS Error in plain words.” |
| --- | --- | --- |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

## Standard config / commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Runtime error | stack / overlay | Null-check; fix import |
| Build fail | deps / tsconfig | Align versions; clear cache |
| Auth/CORS | network tab | Headers and tokens |

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

## When NOT to use

- Skip when a simpler existing approach already fits.

## Related

[[NextJS]]
