**Time take for system to respond to a request.**
"How long does the user/request have to wait before getting a response?"

What contributes to Latency?
- Client sends request
- Network carries request
- Server (Application server, Database server) process request
- Response Travels back
- 

> The total elapsed time experienced by the request

|term|definition|
|-|-|
|Processing Time| is only the time the system spends doing work.|
|Latency|is the time from the request begin sent until the response is received.|

## Latency Components/Decomposition
- Propagation
- Transmission
- Processing
- Queueing 
- Serialization/deserialization

## Types
- [[Network latency]]
- [[Disk storage latency]] The time required for a storage system to read or write data.
- Database latency
- CPU/application latency
- Human-perceived latency

## Measuring Latency (Performance distribution)
Shows how latency should be quantified in real systems.
- Average hides unusual delays
- p50
- p95 
- p99 reveals long-tail delays
- Tail latency

## Reducing Latency

[[Cache]] for repeated data
- Reduce unnecessary network round trips
- Process requests closer to users
- Optimize slow database queries
- Remove unnecessary work

## Latency in Distributed systems
