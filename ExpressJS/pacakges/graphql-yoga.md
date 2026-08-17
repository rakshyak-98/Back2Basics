[[graphql]] [[express concepts]] [[Socket IO]] [[express error handler]]

# graphql-yoga

> GraphQL Yoga is a batteries-included GraphQL HTTP server on Envelop plugins — schema plus resolvers, mount on Node or beside Express, with defaults for landing page and error masking.

```txt
        graphql-yoga ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers contrast REST and GraphQL: context factories, N+1 queries, query…

## Sources
- [GraphQL Yoga documentation](https://the-guild.dev/graphql/yoga-server/docs) — deep-dive
- [GraphQL — Learning](https://graphql.org/learn/) — overview
- [Envelop — Plugin hub](https://the-guild.dev/graphql/envelop) — overview

## Key Concepts
- **Schema + resolvers:** types declare the contract; resolvers implement fields.
- **Envelop plugins:** authentication, caching, logging — compose without forking the server.
- **Context factory:** per-request dependencies (user, loaders) — avoid globals.
- **Error masking:** clients get safe messages; servers log details.
- **HTTP status:** many GraphQL errors still use 200 with an `errors` array


- **Core:** Yoga creates an HTTP handler from a schema (type definitions + resolvers) and…

## Technical Details
```txt
typeDefs + resolvers ──createYoga──► HTTP /graphql endpoint
                              ↕
                    Envelop plugins (authentication, caching, logging)
```

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
| Context factory | Per-request authentication and DataLoaders |
| Error masking | Do not leak stack traces to clients |
| Depth / cost limits | Stop unbounded nested queries |

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| CORS errors in browser | Missing CORS headers | CORS plugin or manual headers |
| N+1 database queries | Resolver loops | DataLoader in context |
| Huge responses | Unbounded queries | Depth and cost limits |
| Authentication missing | Empty context | Session or JWT in context factory |

- Disable introspection in production when policy requires it.

## Mistakes to Avoid
- **Mistake:** Assuming HTTP status always reflects GraphQL field errors
- **Mistake:** Skipping DataLoader and shipping N+1 to production
- **Mistake:** Leaving introspection and verbose errors enabled in production
- **Mistake:** Putting secrets on the root context object shared across requests

## Pros/Cons or Trade-offs
- **Pro:** Strong defaults and plugin ecosystem — faster than wiring Apollo Server from scratch.
- **Con:** Unbounded client queries become an operational risk without limits.
- **Con:** CDN caching and status-based monitoring are harder than REST.

## Comparison
- vs REST [[express concepts]]: REST uses many URLs and status codes
- vs Apollo Server: overlapping space; Yoga emphasizes Envelop plugin composition.
- vs [[Socket IO]]: Yoga is request/response GraphQL; Socket.IO is realtime events.


### Use cases
- Product APIs with nested graphs (users → orders → line items), BFF layers for…

- **Example:** A `user.posts.comments` query hammers the database
