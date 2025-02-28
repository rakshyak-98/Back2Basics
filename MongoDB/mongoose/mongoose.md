### What happens when you interact with MongoDB through mongoose
- mongoose interprets the connection string and manages how to communicate with the database.
### Parsing the connection string
- When you call `mongoose.connect`, Mongoose parses the provided MongoDB connection string. The connection string typically looks like this
```txt
mongodb://username:password@host:port/database
```
### Create a connection
- after parsing the connection string, Mongoose creates a connection instance using the MongoDB NodeJS driver.
- this involves:
	-  a TCP


### mongoose virtuals
- mongoDB itself does not have the concept of virtuals. Virtual properties are a mongoose-only feature, implemented at the application level, not at the database level.
#### Why mongoDB does not have virtuals
- mongoDB stores raw JSON-like documents (BSON) and does not support computed fields natively.
- mongoose which is an ODM (Object-Document Mapper) for mongoDB, provides virtuals as a way to define computed properties on JavaScript objects that are derived from stored data.

> [!INFO] if you want computed fields, you have to use aggregation pipelines or computed fields at the application level.
