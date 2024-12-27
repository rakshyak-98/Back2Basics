`lean()` 
Avoid the overhead of Mongoose wrapper functions and features.
- used in Mongoose ORM to optimize performance for read-heavy opeartions.
- can not use methods like `.save()` or `.validate()` on lean query results.
- read-only use, not suitable for operations requiring updates or additional mongoose methods.

> [!NOTE] as `populate()` normally returns Mongoose documents. When combined with `lean()`, it ensures even the populated fields are returned as plain JavaScript objects.