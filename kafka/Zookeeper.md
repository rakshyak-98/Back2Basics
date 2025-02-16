is a [[distributed coordination service]] used by kafka to manage metadata, leader election, and synchronization across brokers.

| Function                 | Description                                                     |
| ------------------------ | --------------------------------------------------------------- |
| Broker management        | Keeps track of active Kafka brokers.                            |
| Leader election          | Determines which broker is the leader for a partition.          |
| Topic metadata           | Stores partition details and configurations.                    |
| Consumer offsets         | Tracks the last read message for consumers (in older versions). |
| Distributed coordination | Ensures synchronized updates across kafka brokers.<br>          |
### How does kafka brokers register with Zookeeper when they start?
### How does Zookeeper assigns a controller broker to manage partition leader?
### How does producers and consumers fetch metadata from Zookeeper to locate topic leaders?

> [!INFO] Kafka 3.0+ supports KRaft (Kafka Raft mode), which eliminates the need for Zookeeper.
- KRaft directly manages metadata, making Kafka more scalable.