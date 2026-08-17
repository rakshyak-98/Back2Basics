[[NodeJS]] [[expressjs]] [[open api specification]] [[HTTP module]]

# graphql

> Query language + runtime — client asks for exact fields; one endpoint serves queries, mutations, and (optionally) subscriptions.





## Interview Relevance
Interviewers use **graphql** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Schema**, **Resolver**, **Mutation**, **Subscription**.

## Sources
- [GraphQL — Learn](https://graphql.org/learn/) — deep-dive
- [Wikipedia — graphql](https://en.wikipedia.org/wiki/graphql) — overview

## Key Concepts
- **Schema:** Types + operations — Contract between client and server.
- **Resolver:** Per-field fetch — N+1 lives here — DataLoader.
- **Mutation:** Writes — Side effects; not idempotent by default.
- **Subscription:** Push updates — Usually WebSocket transport.

## Technical Details
```txt
Query → parse/validate → resolve fields → JSON
```

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

## Real-World Applications
In production APIs and tooling, **graphql** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **GraphQL ≠ free REST replacement** — caching, file upload, and CDN patterns differ; **Introspection in prod** — disable or protect unless you want a public schema map.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Query language + runtime — client asks for exact fields; one endpoint serves que…).
- **Con / when not:** **Simple CRUD + CDN caching** — REST/OpenAPI often simpler.
- **Con / when not:** **File-heavy APIs** — prefer signed upload URLs + separate storage.

## Comparison
vs [[expressjs]]: know when each applies — do not treat them as interchangeable. vs [[open api specification]]: know when each applies — do not treat them as interchangeable. vs [[HTTP module]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **GraphQL ≠ free REST replacement** — caching, file upload, and CDN patterns differ.
- **Introspection in prod** — disable or protect unless you want a public schema map.
- **Slow list fields:** check N+1 resolvers; fix: DataLoader / join
- **Huge payloads:** check Over-fetching; fix: Stricter schema; query cost
- **Auth leaks:** check Resolver forgot check; fix: Auth at field or directive
- **Schema drift:** check Client vs server; fix: CI schema checks
