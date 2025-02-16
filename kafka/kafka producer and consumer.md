A kafka producer is a component responsible for sending messages (events) to Kafka topics.
- used to notify other microservices (e.g., Inventory, Order, and Discount services).

Decouples services -> ensure [[event-driven]] architecture, reducing direct dependencies between services.

Asynchronous processing -> improves performance by processing cart updates in the background.


### Why disconnect is called each time?
In, Kafka, the `disconnect` is called each time a producer is instantiated and sends a message if a new connection is created and closed immediately rather than being 

#### Short lived producer
- if the kafka producer is instantiated inside a function and not reused, it will create a new connection each time a message is sent.
```js
const {Kafka} = require("kafkajs");

const kafka = new Kafka({
	clientId: 'cart-service',
	brokers: ["localhost:9092"], // Actual Kafka brokers
})

const producer = kafka.producer();

const kafkaProducer = async(topic, message) => {
	await producer.connect();
	await producer.send({
		topic,
		message: [{value: JSON.stringify(message)}],
	});
	await producer.disconnect(); // Disconnects after each message.
}

module.exports = kafkaProducer;
```
- Fix: Reuse the producer instance instead of creating a new one.

```js
const addToCart = async (req, res) => {
	const { userId } = req.auth;
	const { productId, quantity } = req.body;
	await kafkaProducer("cart.item.added", {userId, productId, quantity});
	res.json({ message: "Item added to cart" })
}
```

| Component      | Placement                                                                       |
| -------------- | ------------------------------------------------------------------------------- |
| Kafka Producer | Called inside API handler (e.g, `addToCart`) to publish events.                 |
| Kafka Consumer | Runs as a background process, listening from `topic` events and updating stock. |
- The Service API still handles user request.
- Kafka decouples services, so Inventory Service automatically updates stock without needing a direct API call.
- More services (e.g., Order, Discount) can consumer the same Kafka event to react accordingly.

## Kafka Consumer
```js

const consumer = kafka.consumer({ groupId: "inventory-group" })

const run = async () => {
	await consumer.connect();
	await consumer.subscribe({ topic: 'cart.item.added' })
	await consumer.run({
		eachMessage: async ({ message }) => {
			cosnt {productId, quantity} = JSON.parse(message.value.toString());
			await db.query( "UPDATE products SET stock = stock - $1 WHERE id = $2", [quantity, productId] )
		}
	})
}

run().catch(console.error);

```
- run independently, listening for `cart.item.added` events.

## Connection pooling not used (Explained Clearly)
Kafka does not have an internal [[connection pool]] like databases, but it does allow persistent connections to brokers. If you not reusing connection efficiently.

#### What happens without connection reuse?
Each time a producer is created:
- It establishes a new TCP connection to the kafka broker.
- It performs authentication (if enabled).
- It sends metadata requests to discover partitions.
- It sends the actual message.
- It closes the connection when `disconnect()` is called.

> [!INFO] This create high latency and extra load on the broker because:
- each message incurs the overhead of creating and tearing down a connection.
- kafka brokers must handle frequent connects/disconnects.
- producers can't batch message efficiently.


```txt
{"level":"WARN","timestamp":"2025-02-16T10:43:42.166Z","logger":"kafkajs","message":"KafkaJS v2.0.0 switched default partitioner. To retain the same partitioning behavior as in previous versions, create the producer with the option \"createPartitioner: Partitioners.LegacyPartitioner\". See the migration guide at https://kafka.js.org/docs/migration-guide-v2.0.0#producer-new-default-partitioner for details. Silence this warning by setting the environment variable \"KAFKAJS_NO_PARTITIONER_WARNING=1\""}
Cart service is running on port 3000
{"level":"ERROR","timestamp":"2025-02-16T10:43:42.204Z","logger":"kafkajs","message":"[Connection] Response Metadata(key: 3, version: 6)","broker":"localhost:9092","clientId":"cart.service","error":"This server does not host this topic-partition","correlationId":1,"size":90}
/home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/protocol/error.js:581
  return new KafkaJSProtocolError(errorCodes.find(e => e.code === code) || unknownErrorCode(code))
         ^
KafkaJSProtocolError: This server does not host this topic-partition
    at createErrorFromCode (/home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/protocol/error.js:581:10)
    at Object.parse (/home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/protocol/requests/metadata/v0/response.js:55:11)
    at Connection.send (/home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/network/connection.js:433:35)
    at processTicksAndRejections (node:internal/process/task_queues:95:5)
    at async Broker.[private:Broker:sendRequest] (/home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/broker/index.js:904:14)
    at async Broker.metadata (/home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/broker/index.js:177:12)
    at async /home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/cluster/brokerPool.js:158:25
    at async /home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/cluster/index.js:111:14
    at async Cluster.refreshMetadata (/home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/cluster/index.js:172:5)
    at async Cluster.addMultipleTargetTopics (/home/ubuntu/GitHub/Playground/express-playground/node_modules/kafkajs/src/cluster/index.js:230:11) {
  retriable: true,
  helpUrl: undefined,
  type: 'UNKNOWN_TOPIC_OR_PARTITION',
  code: 3,
  [cause]: undefined
}

```
- possible causes, topic doesn't exist, broker metadata is outdated, partitions are not assigned properly, ensure correct kafka connection

##### Fix the Partitioner warning
```js
const producer = kafka.producer({
  createPartitioner: Partitioners.LegacyPartitioner,
});

```


```txt
{"level":"ERROR","timestamp":"2025-02-16T10:54:00.249Z","logger":"kafkajs","message":"[Connection] Connection error: getaddrinfo EAI_AGAIN kafka-server","broker":"kafka-server:9092","clientId":"cart.service","stack":"Error: getaddrinfo EAI_AGAIN kafka-server\n at GetAddrInfoReqWrap.onlookup [as oncomplete] (node:dns:107:26)"}
```
- the error `getadderinfo EAI_AGAIN kafka-server`  means the Kafka client cannot resolve the hostname `kafka-server`