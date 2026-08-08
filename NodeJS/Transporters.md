[[Application layer]] [[MQTT]] [[gRPC]] [[HTTP]]

# Transporters

> Transporters — abstraction over data transmission they handle how data moves between systems / components.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Architecture & Lifecycle Mechanics]]
- [[#Microservice Transporters (Message Brokers & RPC)]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Transporters abstraction over data transmission they handle how data moves between systems / components.
- Transporters in backend code typically refer to modules that abstract how data or messages are send and received between systems or components.
> [!INFO] You'd use a transporter to decouple your business logic from the specifics of communication.
- You want to switch between protocols (HTTP, WebSockets, TCP, NATS kafka, etc.) without rewriting your app logic.
- A Transporter defines an interface like `send(data)` or `emit(event)` and handles all the low-level details.
- They encapsulate the complexity of raw TCP/UDP/UDS socket management, providing a unified interface for data transmission across various protocols (HTTP, gRPC, AMQP, MQTT).

## Standard config / commands

…

## Architecture & Lifecycle Mechanics

## Microservice Transporters (Message Brokers & RPC)

[[Message Broker]] [[RPC]]

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
