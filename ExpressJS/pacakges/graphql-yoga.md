[[ExpressJS]] [[graphql]] [[express concepts]]

# graphql-yoga

> GraphQL Yoga is a batteries-included GraphQL server built on Envelop plugins — define a schema and resolvers, mount on Node HTTP or alongside Express/Fastify, with sensible defaults for landing page and error masking.

---

## Architecture

```txt
typeDefs + resolvers ──createYoga──► HTTP /graphql endpoint
                              ↕
                    Envelop plugins (auth, caching, logging)
```

Yoga handles HTTP transport, GraphQL execution, and plugin composition. Context factory is where authentication and database connections attach.

---

## Standalone server

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
|------|----------------|
| `graphqlEndpoint` | Path (default `/graphql`) |
| Context factory | Per-request auth and data loaders |
| Error masking | Do not leak stack traces to clients |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| CORS errors in browser | Missing CORS headers | CORS plugin or manual headers |
| N+1 database queries | Resolver loops | DataLoader in context |
| Huge responses | Unbounded queries | Depth and cost limits |
| Auth missing | Empty context | JWT or session in context factory |

GraphQL often returns **200 with errors in the body** — unlike REST status-per-error patterns. Disable introspection in production if policy requires.

---

## When GraphQL Yoga is a poor fit

- Simple CRUD with CDN caching — REST may be simpler.
- File-upload-only APIs — dedicated upload service.
- Teams without schema discipline — unbounded client queries become operational risk.

---

## Related

[[graphql]] · [[express concepts]] · [[Socket IO]]
