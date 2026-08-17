[[kafka]] [[Kafka broker]] [[Kafka configuration]] [[distributed system]]

# Zookeeper

> Distributed coordination service — historically stored Kafka’s cluster metadata and helped elect controllers; new clusters prefer KRaft instead.





## Interview Relevance
Interviewers ask about ZooKeeper to see if you understand *why* Kafka needed an external ensemble (metadata, membership, controller election) and what changes when Kafka runs in KRaft mode without it.

## Sources
- [Apache ZooKeeper documentation](https://zookeeper.apache.org/doc/current/) — deep-dive
- [Apache Kafka — KRaft vs ZooKeeper](https://kafka.apache.org/43/getting-started/zk2kraft/) — deep-dive
- [Wikipedia — Apache ZooKeeper](https://en.wikipedia.org/wiki/Apache_ZooKeeper) — overview

## Core Definition
Apache ZooKeeper is a CP-leaning coordination store: small znodes, watches, and leader election primitives. Classic Kafka clusters used a ZooKeeper ensemble for broker registration, controller election, and topic metadata (offsets moved to Kafka topics long ago).

## Key Concepts
- **Ensemble:** odd-sized cluster (3/5) for quorum → survives minority failure.
- **znode + watch:** clients watch paths for membership and configuration changes → notification-driven coordination.
- **Kafka controller election:** one broker becomes controller via ZooKeeper → manages partition leaders (legacy mode).
- **Metadata bottleneck:** large partition counts stressed ZooKeeper → motivation for KIP-500 / KRaft.
- **Migration:** Kafka 3.x supports ZooKeeper→KRaft migration; Kafka 4.x line removes ZooKeeper mode.

## Technical Details
| Kafka function (ZK mode) | Role of ZooKeeper |
|--------------------------|-------------------|
| Broker membership | Ephemeral znodes for live brokers |
| Controller election | Elects which broker manages leadership |
| Topic metadata | Partition assignments and configurations |
| Legacy offsets | Older versions stored offsets in ZK (now Kafka `__consumer_offsets`) |

Broker start (conceptual): register under `/brokers/ids`, watch cluster state, follow controller decisions for partition leaders.

```bash
# ZooKeeper CLI examples (ensemble must be reachable)
zkCli.sh -server localhost:2181
ls /brokers/ids
get /controller
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Kafka cannot elect controller | ZK quorum / disk | Restore ensemble; check ZXID / disk full |
| Split-brain fears | Ensemble size even | Run 3 or 5 nodes, not 2 |
| Slow admin operations | ZK latency | Isolate ZK disks; plan KRaft migration |

## Real-World Applications
Legacy Kafka clusters still run ZooKeeper ensembles; other systems (HBase, older Solr) also used it for coordination. Greenfield Kafka should use KRaft ([[Kafka configuration]]).

**Example:** A three-node ZooKeeper ensemble backs a Kafka 2.x cluster; operators monitor ZK latency as carefully as broker disk.

## Pros/Cons or Trade-offs
- **Pro:** Battle-tested coordination primitives; well understood operationally for older stacks.
- **Con:** Extra moving part beside Kafka — more failure domains and tuning.
- **Con:** Partition-scale limits pushed the ecosystem to KRaft.

## Comparison
- vs KRaft: metadata lives in a Kafka Raft quorum of controllers — no external ZK.
- vs etcd/Consul: similar coordination niche; Kafka’s path is KRaft, not swapping etcd under brokers.

## Mistakes to Avoid
- Running a single ZooKeeper node in production “for simplicity.”
- Ignoring ZK disk/latency while only watching Kafka broker CPU.
- Starting a new Kafka 4.x deployment with ZooKeeper mode (removed / unsupported path).
