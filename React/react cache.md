# TenStack Query
### updating cache from mutation
if you make a mutation toward a single specific resource, and you know that it will update only that specific resource, you could directly update the cache from the `onSuccess` callback
- use the response from the API in the mutation to update the cached query, which in turn will re-render any component using the original query.
#### Optimistic update
- when we send the mutation to the server, we also update the local cache with what we expect the server to do. If we add something, we can add the same thing locally; if we delete something, we delete the same thing locally, and so on.
- if the server request fails, we immediately roll back any optimistic updates that we performed and revert to whatever the cache state was before we started the request.