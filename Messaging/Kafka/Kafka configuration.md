<!-- note-strategy: operational -->
[[Kafka]]

# Kafka configuration

> Kafka configuration — kafka 08:14:27.57 ERROR ==> Kafka haven't been configured to work in either Raft or Zookeper mode. Please make sure at least one of…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Kafka configuration — kafka 08:14:27.57 ERROR ==> Kafka haven't been configured to work in either Raft or Zookeper mode. Please make sure at least one of…

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


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[Kafka]]
