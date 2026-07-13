[[Application layer]] [[MQTT]] [[gRPC]] [[HTTP]]

Transporters abstraction over data transmission they handle how data moves between systems / components.

- Transporters in backend code typically refer to modules that abstract how data or messages are send and received between systems or components.

> [!INFO] You'd use a transporter to decouple your business logic from the specifics of communication.

- You want to switch between protocols (HTTP, WebSockets, TCP, NATS kafka, etc.) without rewriting your app logic.
- A Transporter defines an interface like `send(data)` or `emit(event)` and handles all the low-level details.

> Transporters are application-layer abstractions responsible for managing network I/O state machines, connection pooling, protocol negotiation, and the serialization/deserialization of payloads between the runtime environment and the underlying network sockets.
- They encapsulate the complexity of raw TCP/UDP/UDS socket management, providing a unified interface for data transmission across various protocols (HTTP, gRPC, AMQP, MQTT).


## Architecture & Lifecycle Mechanics

## Microservice Transporters (Message Brokers & RPC)

[[Message Broker]] [[RPC]]