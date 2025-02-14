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

