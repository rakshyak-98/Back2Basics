A broker in Apache Kafka is server that acts as an intermediary between producers (who send messages) and consumers (who receive messages).

| feature              | Description                                                       |
| -------------------- | ----------------------------------------------------------------- |
| Message storage      | Stores messages in topics and partitions.                         |
| Message routing      | Distributes messages from producers to consuers.                  |
| partition Management | handles partition assignments and replications.                   |
| Load balancing       | Spreads workload across multiple brokers in a kafka cluster.      |
| Replication          | Ensures fault tolerance by duplicating partitions across brokers. |
### Why is it called a Topic in Kafka?
The term _topic_ in kafka is inspired by publish-subscribe messaging systems.
- it represents a logical channel where messages are categorized, similar to how topics work in forums or newsletters.