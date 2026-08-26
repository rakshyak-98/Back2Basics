instead of create separate table for different user entity, define a same type of entity represent relationship using (points back to another row) foreign key **self-referencing foreign key**.

- flexibility. The database does not need a separate table for every hierarchy level.
- If new hierarchy level is needed the database structure does not necessarily need to change. A new role can be introduced maintaining the same parent-child relationship.
- Two user can have same role while belonging to completely different branches of the hierarchy.

### Recursive traversal can become expensive
- Moving a user or an entire sub-tree. If a user is moved to another parent, the application must ensure that the move does not create invalid relationships or cycles.

this must be prevented
```txt
A -> B -> C -> A
```
- A user cannot ultimately become their own ancestor.

A separate table stores ancestor-descendant relationships. This is useful when application frequently perform complex hierarchy queries.