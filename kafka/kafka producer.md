A kafka producer is a component responsible for sending messages (events) to Kafka topics.
- used to notify other microservices (e.g., Inventory, Order, and Discount services).

Decouples services -> ensure [[event-driven]] architecture, reducing direct dependencies between services.

Asynchronous processing -> improves performance by processing cart updates in the background.

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
	await producer.disconnect();
}

module.exports = kafkaProducer;
```

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
