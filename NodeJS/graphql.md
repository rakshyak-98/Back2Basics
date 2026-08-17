[[NodeJS]] [[expressjs]] [[open api specification]] [[HTTP module]]

# graphql

> Query language + runtime — client asks for exact fields; one endpoint serves queries, mutations, and (optionally) subscriptions.

```txt
        graphql ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **graphql** to check whether you can explain the mechanism i…

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

## Mistakes to Avoid
- **Mistake:** **GraphQL ≠ free REST replacement**
- **Mistake:** **Introspection in prod**
- **Mistake:** **Slow list fields:** check N+1 resolvers; fix: DataLoader / join
- **Mistake:** **Huge payloads:** check Over-fetching
- **Mistake:** **Auth leaks:** check Resolver forgot check
- **Mistake:** **Schema drift:** check Client vs server; fix: CI schema checks

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Query language + runtime — client asks for exact fields; one endpoint serves que…).
- **Con / when not:** **Simple CRUD + CDN caching**
- **Con / when not:** **File-heavy APIs**

## Comparison
- vs [[expressjs]]: know when each applies


### Use cases
- In production APIs and tooling, **graphql** shows up whenever teams ship Node…
