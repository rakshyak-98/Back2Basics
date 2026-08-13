[[NodeJS]] [[expressjs]] [[open api specification]]

# graphql

> Query language + runtime — client asks for exact fields; one endpoint serves queries, mutations, and (optionally) subscriptions.

---

## How it works

```txt
Query → parse/validate → resolve fields → JSON
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Schema** | Types + operations | “Contract between client and server.” |
| **Resolver** | Per-field fetch | “N+1 lives here — DataLoader.” |
| **Mutation** | Writes | “Side effects; not idempotent by default.” |
| **Subscription** | Push updates | “Usually WebSocket transport.” |


## Configuration and commands

```js
import { ApolloServer } from '@apollo/server'
import { startStandaloneServer } from '@apollo/server/standalone'

const typeDefs = `#graphql
  type Query { hello: String }
`
const resolvers = { Query: { hello: () => 'world' } }
const server = new ApolloServer({ typeDefs, resolvers })
await startStandaloneServer(server, { listen: { port: 4000 } })
```

| Knob | Why it matters |
|------|----------------|
| Depth/complexity limits | Stop expensive queries |
| Persisted queries | Smaller payloads + allowlists |
| DataLoader | Batch/cache per request |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow list fields | N+1 resolvers | DataLoader / join |
| Huge payloads | Over-fetching | Stricter schema; query cost |
| Auth leaks | Resolver forgot check | Auth at field or directive |
| Schema drift | Client vs server | CI schema checks |

---


## Gotchas

> [!WARNING]
> **GraphQL ≠ free REST replacement** — caching, file upload, and CDN patterns differ.

> [!WARNING]
> **Introspection in prod** — disable or protect unless you want a public schema map.

---


## When not to use

- **Simple CRUD + CDN caching** — REST/OpenAPI often simpler.
- **File-heavy APIs** — prefer signed upload URLs + separate storage.

---


## Related

[[expressjs]] [[open api specification]] [[HTTP module]]

## Sources

- [Wikipedia — graphql](https://en.wikipedia.org/wiki/graphql)
