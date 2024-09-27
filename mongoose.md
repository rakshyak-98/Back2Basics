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