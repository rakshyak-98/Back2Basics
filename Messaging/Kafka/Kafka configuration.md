[[kafka]] [[Kafka broker]] [[Zookeeper]] [[kafka producer and consumer]]

# Kafka configuration

> Settings that decide how brokers and clients run — especially KRaft versus ZooKeeper mode, listeners, and advertised addresses that clients actually dial.

```txt
        Kafka configuratio ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers and take-home labs often break on *advertised listeners* and “ne…

## Sources
- [Apache Kafka — KRaft](https://kafka.apache.org/43/operations/kraft/) — deep-dive
- [Bitnami Kafka container docs](https://github.com/bitnami/containers/blob/main/bitnami/kafka/README.md) — overview
- [Kafka broker configs](https://kafka.apache.org/documentation/#brokerconfigs) — deep-dive

## Key Concepts
- **KRaft mode:** `process.roles` includes `broker` / `controller`
- **ZooKeeper mode (legacy):** `zookeeper.connect` points at an ensemble
- **Listeners vs advertised.listeners:** bind address inside the container/network versus what *clients* use to reconn…
- **Combined role:** one process as broker+controller
- **Client configs:** `bootstrap.servers`, `group.id`, `acks`, serializers


- **Core:** Kafka configuration is the set of broker/controller and client properties (fi…

## Technical Details
- Common container error when neither mode is set:

```text
ERROR ==> Kafka haven't been configured to work in either Raft or Zookeeper mode.
Please make sure at least one of the modes is configured.
```

- **KRaft single-node lab (Bitnami-style environment variables):** 

```shell
docker network create app-tier

docker run -d --name kafka-server -p 9092:9092 --hostname kafka-server \
  --network app-tier \
  -e KAFKA_CFG_NODE_ID=0 \
  -e KAFKA_CFG_PROCESS_ROLES=controller,broker \
  -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
  -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
  -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://192.168.1.10:9092 \
  -e KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-server:9093 \
  -e KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  bitnami/kafka:latest
```

- Use a reachable host IP (or Docker DNS name) in `ADVERTISED_LISTENERS`

| Symptom | Check | Fix |
|---------|-------|-----|
| Neither Raft nor ZK mode | `process.roles` / ZK connect | Set KRaft roles *or* legacy ZK (version permitting) |
| Client connects then fails | Advertised listener | Publish an address the client can route to |
| Controller unstable | Quorum voters mismatch | Align node ids and `@host:port` voters |
| Auth handshake fail | Security protocol map | Match SASL/SSL on listener and client |

## Mistakes to Avoid
- **Mistake:** Advertising the container’s internal hostname to clients running…
- **Mistake:** Copy-pasting ZooKeeper environment variables into a Kafka 4.x im…
- **Mistake:** Using combined mode in production without a plan for controller …

## Pros/Cons or Trade-offs
- **Pro:** Explicit listeners make multi-network topologies possible (internal + external).
- **Con:** Easy to misconfigure; symptoms appear as intermittent client metadata errors.
- **Con:** Combined controller+broker simplifies demos but couples failure domains.

## Comparison
- vs [[Zookeeper]]: configuration either points at ZK (legacy) or defines KRaft roles
- vs [[kafka producer and consumer]]: broker configuration is cluster-side


### Use cases
- Local Docker Compose for developers, and Helm/operators in Kubernetes that in…

- **Example:** Developers hit `localhost:9092` while brokers advertised `kafka:…
