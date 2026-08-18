[[ExpressJS]] [[graphql]] [[express concepts]]

# graphql-yoga

> GraphQL Yoga — batteries-included GraphQL server (Envelop plugins) that mounts on Node/HTTP or alongside Express/Fastify.

## Mental model

**Say it in one breath:** Define schema + resolvers; Yoga serves `/graphql` with useful defaults (landing page, error masking). Compose plugins for authentication/caching.

```txt
schema + resolvers ──Yoga──► HTTP GraphQL endpoint
```

## Standard config / commands

```js
import { createSchema, createYoga } from 'graphql-yoga'
import { createServer } from 'http'

const yoga = createYoga({
  schema: createSchema({
    typeDefs: `type Query { hello: String! }`,
    resolvers: { Query: { hello: () => 'hi' } },
  }),
})
createServer(yoga).listen(4000)
```

| Knob | Why it matters |

| `graphqlEndpoint` | Path |
| --- | --- |
| Context factory | Auth/db |
| Masking errors | Don’t leak stacks |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| CORS | Browser clients | CORS plugin/headers |
| N+1 | Resolver loops | DataLoader |
| Huge payloads | Unbounded queries | Depth/cost limits |
| Auth missing | Context | JWT/session in context |

## Gotchas

> [!WARNING]
> **GraphQL ≠ REST status codes** — errors in body often with 200.

> [!WARNING]
> **Introspection in prod** — disable if policy requires.

## When NOT to use

- **Simple CRUD with caching CDNs** — REST may be simpler.
- **File upload only APIs** — dedicated upload service.
- **Teams without schema discipline** — chaos.

## Related

[[graphql]] [[express concepts]] [[Socket IO]]
