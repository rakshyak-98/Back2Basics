```txt
kafka 08:14:27.57 ERROR ==> Kafka haven't been configured to work in either Raft or Zookeper mode. Please make sure at least one of the modes is configured.
```

- Zookeeper mode -> Traditional mode with a zookeeper cluster managing brokers.
- KRaft mode -> Newer mode where kafka manages metadata internally.

```shell
docker run -d --name kafka-server --hostname kafka-server \
    --network app-tier \
    -e KAFKA_CFG_NODE_ID=0 \
    -e KAFKA_CFG_PROCESS_ROLES=controller,broker \
    -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
    -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
    -e KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-server:9093 \
    -e KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER \
    bitnami/kafka:latest
```
- create docker network first then run this command

##### Kafka client instance
```shell
docker run -it --rm \
    --network app-tier \
    bitnami/kafka:latest kafka-topics.sh --list  --bootstrap-server kafka-server:9092
```
- Launch your Apache kafka client instance