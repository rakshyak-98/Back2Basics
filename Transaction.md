A transaction is a way for application to group several reads and writes together into a logical unit. 

With transactions, error handling becomes much simpler for an application, because it doesn't need to worry about partial failures (where, for whatever reason, some operations succeed and some fail).

*Safety guarantees* Using transaction allows the application to ignore certain potential error scenarios and concurrency issues, because the database takes care of them instead. 

**How do you figure out whether you need transactions?**

> The transactional system can scale to large data volumes and high throughput

[[Atomicity]]