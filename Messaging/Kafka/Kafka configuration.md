```txt
kafka 08:14:27.57 ERROR ==> Kafka haven't been configured to work in either Raft or Zookeper mode. Please make sure at least one of the modes is configured.
```

- Zookeeper mode -> Traditional mode with a zookeeper cluster managing brokers.
- KRaft mode -> Newer mode where kafka manages metadata internally.

```shell
docker run -d --name kafka-server -p 9092:9092 --hostname kafka-server \ 
	--network app-tier \ 
	-e KAFKA_CFG_NODE_ID=0 \
	-e KAFKA_CFG_PROCESS_ROLES=controller,broker \
	-e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
	-e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
	-e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://192.168.1.10:9092 \ # use host ip (local maching not docker container)
	-e KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-server:9093 \
	-e KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER \
bitnami/kafka:latest
```
- create docker network first then run this command

##### Kafka client instance
```shell
docker run -d --name kafdrop -p 9000:9000 --network app-tier   -e KAFKA_BROKERCONNECT=kafka-server:9092   obsidiandynamics/kafdrop

```
- Launch your Apache kafka client instance
- kafdrop must be on the same Docker network as Kafka

> [!NOTE] If you are using `bitnami/kafka` in Docker, the scripts like `kafka-config.sh` and `kafka-topics.sh` are not in the default path. You need to execute them inside the container.

```txt
#
#Sun Feb 16 08:44:24 UTC 2025
node.id=0
directory.id=DNf6f5byQ4QLOL7id62iDw #Ensures correct partition recovery after a restart.
version=1 #file format version
cluster.id=1Sl9qzLGSm-_UgDgtgp6hw #used to prevent from joining the wrong cluster.

```
- `meta.properties` which is stored in the log directory
- contains essential metadata for the broker's identity within the cluster.

> [!INFO] In kafka, an entity type refers to the type of resource whose configuration you want to manage. The error `At least one entity type must be specified` occurs when you run `kafka-configs.sh` without specifying an entity type.

### Check Running Processes with zookeeper or KRaft

Run inside your Kafka container:
```shell
kafka-config.sh --describe --entity-type brokers --bootstrap-server kafka-server:9092 --all | grep process;
```
- If you see `-Dzookeeper.connect=...` ➝ Using **Zookeeper**
- If you see `-Dprocess.roles=controller,broker` ➝ Using **KRaft**


> [!INFO] `PLAINTEXT://` in Kafka is a Kafka protocol identifier used in the `listeners` and `advertised.listeners` settings. It specifies that Kafka will use un-encrypted communication over _TCP_.

#### Other Kafka protocols

| Protocol       | Description                                    |
| -------------- | ---------------------------------------------- |
| `PLAINTEXT://` | No encryption (default)                        |
| `SSL://`       | User TLS/SSL encryption                        |
| `SASL_SSL://`  | Users SASL authentication + SSL encryption<br> |
`listeners` -> where kafka listens for connections.
`advertised.listeners` -> the external address kafka tells clients to connect to.

### Why `advertised.listeners` is important
Kafka brokers often run in Docker, Kubernetes, or cloud environments, where the internal address (`listeners`) differs from the external address clients need to connect to.

### Expected behavior Based on setup

| Setup                        | Effect of `advertised.listeners=null`                                                    |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| Local Kafka (single machine) | Works fine (uses `listeners` address)                                                    |
| Docker (bridge mode)         | Clients outside the container can't connect (Kafka advertises the internal container IP) |
| Docker (host mode)           | Works fine (users host IP)                                                               |
| Kubernetes                   | Clients may get wrong pod IP instead of service DNS                                      |
| Multi-node Kafka Cluster     | Brokers may advertise wrong internal addresses, breaking inter-broker communication<br>  |
If Kafka is in Docker bridge mode, you need to explicitly set `advertised.listeners`
```text
listeners=PLAINTEXT://0.0.0.0:9092
advertised.listeners=PLAINTEXT://192.168.1.100:9092
```
- kafka listens inside the container on `0.0.0.0:9092`
- External clients connect using the host IP `192.168.1.100`