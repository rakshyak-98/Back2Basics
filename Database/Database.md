## Relational Databases

A relational database organizes data into **tables**, where each table has a defined **schema** that describes its columns and data types.

Tables can have **relationships** with each other, which are established using **primary keys and foreign keys**.

A primary key uniquely identifies a row in a table, while a foreign key creates a link between related tables.

Relational databases are designed to reduce **data redundancy** by normalizing data and storing related information in separate tables.

The structured nature of relational databases makes the data **predictable and organized**, which makes them useful when the relationships between different pieces of data are well defined.

### ACID Properties

Relational databases commonly provide **ACID transactions**, which ensure reliable and consistent data operations.

* **Atomicity** means that a transaction is treated as a single unit: either all of its operations succeed, or none of them are applied.
* **Consistency** means that a transaction takes the database from one valid state to another valid state while maintaining defined rules and constraints.
* **Isolation** means that concurrent transactions do not interfere with each other or see intermediate changes made by other transactions.
* **Durability** means that once a transaction has been successfully committed, the data remains saved even if the system crashes afterward.

### Scaling Challenges

As a relational database grows, scaling can become challenging because the database has a **rigid schema** and complex relationships between tables.

Changing the schema or distributing relational data across multiple machines can become more difficult as the system grows.

Popular relational databases include **PostgreSQL, MySQL, and Oracle Database**.

---

## NoSQL Databases

NoSQL databases provide greater **flexibility** on schema design. Than relational databases and are designed to handle different data models and large-scale workloads.

They generally use **flexible schemas**, which makes it easier to store data whose structure may change over time.

NoSQL databases are often designed with **horizontal scalability and high availability** in mind, allowing data and workloads to be distributed across multiple machines.

Different NoSQL databases are optimized for different data models, such as **document, wide-column, key-value, graph, and time-series data**.

---

## Document Database

A document database stores data as **documents**, commonly using formats such as JSON.

Related data can be stored together inside the same document, which provides **data locality** and can make read operations faster because the application does not need to perform multiple joins to retrieve related data.

Documents with similar structures are typically stored in the same **collection**.

The downside is that storing related data together can lead to **data duplication and denormalization**.

Many document databases also support **multi-document ACID transactions** when an operation needs to update multiple documents atomically.

---

## Wide-Column Database

A wide-column database stores data in rows, but unlike a traditional relational database, **different rows do not necessarily need to contain the same columns**.

This allows each row to have its own set of columns based on the data being stored.

Wide-column databases are designed for **massive-scale distributed workloads** and can distribute data across many machines.

Some systems support **multi-leader or leaderless architectures**, which can make them highly resilient to individual node failures.

Because there can be multiple write points, these systems often use mechanisms such as **conflict resolution** to determine which version of the data should be considered authoritative.

For example, Cassandra can use a **last-write-wins** strategy to resolve conflicting writes.

Wide-column databases are often optimized for **high write throughput**.

Many of them use **LSM-tree-based storage engines**, where writes are first accumulated in memory and then flushed to disk in batches.

This approach can provide very efficient write performance and is particularly useful for workloads involving large volumes of sequential writes.

---

## Key-Value Database

A key-value database stores data as a **unique key associated with a value**.

For example, Redis can store a value using a unique key and retrieve that value directly using the key.

Redis primarily keeps data **in memory**, which allows extremely fast read and write operations by avoiding the latency of accessing disk for every operation.

Key-value stores are commonly used for **caching**, where frequently accessed data is moved from a slower primary data store into a faster cache.

They are particularly useful for **real-time applications and high-frequency lookups**, especially when the cached dataset can fit efficiently in memory.

---

## Graph Database

A graph database is designed to store and navigate **relationships between data points**.

Instead of treating relationships as something that must be reconstructed through joins, a graph database stores relationships directly between nodes.

For example, finding an indirect relationship between two users in a relational database may require multiple SQL joins.

In a graph database, the system can directly traverse the relationships between connected nodes.

Graph traversal can be very efficient because the database follows the existing relationships rather than scanning the entire dataset.

Graph databases are commonly used for **fraud detection, recommendation systems, social networks, and knowledge graphs**.

They also typically provide a **specialized query language** for expressing graph traversals and relationship-based queries.

---

## Time-Series Database

A time-series database is optimized for storing and querying data that is associated with **timestamps**.

For example, InfluxDB is designed specifically for time-series workloads.

These databases typically optimize indexes and storage structures around **time-based queries**, making it efficient to retrieve data for a particular time range.

They are commonly used for **IoT systems, sensor readings, application monitoring, and system metrics**.

Time-series databases can also partition data based on time, which makes operations such as querying recent data and deleting old data more efficient.

They are particularly useful for analyzing **trends over time**, such as understanding sales trends, monitoring system health, or analyzing sensor behavior.

---

## Database Indexing

An **index** is an additional data structure that helps a database find rows more efficiently without scanning the entire table.

A **secondary index** can be created on columns that are frequently used for filtering, sorting, or searching.

For example, if applications frequently query users by email address, an index on the email column can allow the database to locate the required row much faster.

However, indexes come with a trade-off.

Although indexes improve **read performance**, they increase the cost of **insert, update, and delete operations** because the database must also maintain the index whenever the underlying data changes.

So, indexes should be created strategically on columns that are frequently used in important queries.