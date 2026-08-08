[[System Design]]

# Throughput

> Throughput — measure of the actual data (bits/payload) successfully transferred from a source to a destination over a specific network path or through a processing pipeline

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

measure of the actual data (bits/payload) successfully transferred from a source to a destination over a specific network path or through a processing pipeline per unit of time.
### API architecture
In API architecture, **throughput** is defined as the number of requests per second (RPS) or transactions per second (TPS) a system can handle while maintaining acceptable latency and error rates. It is the metric of system capacity under load.
**The Throughput Hierarchy**
- Network/Connection layer -> The number of TCP handshakes and TLS negotiations the load balancer or web server can handle.
	- Bottleneck context switching and memory limits for open file descriptors.
- Application/Logic Layer -> The speed at which your code processes the request payload.
	- Bottleneck Serialization/Deserialization (SerDes) costs, specifically JSON/Protobuf parsing overhead.
- Resource / I/O Layer -> The interaction with external state (e.g., writing to a DB or triggering an NVENC session)
	- Bottleneck Blocking calls; if an API endpoint waits for a GPU handle to be allocated, that request block an execution thread, limiting total system throughput.

## Standard config / commands

…

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
