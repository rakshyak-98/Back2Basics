Kafka is a distributed event streaming platform used for real-time data processing. 
- it helps microservices communicate asynchronously by sending and receiving messages efficiently.

### How kafka works
kafka consist of four main components

| Component | Description                                                    |
| --------- | -------------------------------------------------------------- |
| Producer  | sends message (events) to kafka topics.                        |
| Topic     | A category where message are stored. Example `cart.item.added` |
| Broker    | Kafka servers that manage topics and messages.                 |
| Consumer  | Listens to topics and process messages.                        |