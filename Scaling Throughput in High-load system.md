[[connection churn]] [[pre-warmed pool]]

For an architecture managing high-density media streams, standard REST/HTTP paradigms often fail due to header overhead and connection churn.

- Batching -> If your API handles configuration for 300 channels, never expose an endpoint that requires 300 individual serial requests. Implement Bulk Endpoints to process state changes in a single transaction, significantly reducing SerDes overhead.
- Asynchronous Processing -> Move state-heavy operations to a background queue. The API should return `202 Accepted` immediately, and the internal worker pool (using a pre-warmed pool of NVENC contexts) handles the heavy lifting.
- Connection Reuse -> Use gRPC over HTTP/2. Unlike traditional REST/HTTP1.1, gRPC maintains connections, reducing the CPU cost of constant TCP/TLS handshakes and enabling multiplexing (sending multiple requests over one stream).


## When API hits a throughput wall, analyze these specific indicators

|**Component**|**Metric to Monitor**|**High-Load Indicator**|
|---|---|---|
|**NIC**|PPS (Packets Per Second)|Kernel interrupt saturation (>50% CPU on softirq)|
|**API Server**|Context Switches|High `cs` rates (indicating thread contention)|
|**GPU/Engine**|NVENC API Latency|Time to open a new session (the "cold start" problem)|
|**Memory**|GC (Garbage Collection)|High memory churn caused by allocating new request objects|

