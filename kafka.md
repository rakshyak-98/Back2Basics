- event streaming platform designed to handle real-time data feeds.
- used for building data pipelines, stream analytics, and integration across systems.
- Scale horizontally by distributing data across multiple brokers.
- producer and consumers are independent, allowing system flexibility.

**Producers**: Send data (message) to Kafka topics.
**Consumers**: Read data from topics.
**Topics**: Logical storage units to organize message. Each topic can have multiple partitions for parallelism.
**Brokers**: Kafka servers managing storage and distribution of topics.
**ZooKeeper (or Kafka Raft)**: Coordinates brokers and maintains cluster metadata.

### kafka docker contianer
