query keys: uniquely identify and manage cache data
- React Query uses query keys to manage and update cache automatically

when we invalidate queries, we're telling React Query that the data in those queries may no longer be accurate because of the mutation.
- invalidation triggers a refetch for any invalidated queries the next time they are accessed. 
- So if a component or action tries to fetch customers again, React query will send a fresh request to the database.
### Mutation
- mutations are typically about changing data (like submitting forms or updating records), they don't need query keys, as they don't automatically cache or update data.
- mutations don't require query keys because they don't directly interact with or update the cache on their own.