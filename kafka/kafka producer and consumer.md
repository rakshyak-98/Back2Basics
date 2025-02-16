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