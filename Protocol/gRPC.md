[[HTTP module]] [[TCP]] [[TLS (Transport Layer Security)]] [[webSocket]]

# gRPC

> gRPC is a high-performance RPC framework over HTTP/2 with Protocol Buffers — strong typing, streaming, and deadlines make it a common default for service-to-service calls.





## Interview Relevance
Interviewers compare gRPC to REST/JSON, expect the four call types, and ask why L7 balancers must be HTTP/2 / gRPC-aware.

## Sources
- [gRPC documentation](https://grpc.io/docs/) — deep-dive
- [Protocol Buffers Language Guide](https://protobuf.dev/programming-guides/proto3/) — overview
- [RFC 9113 — HTTP/2](https://datatracker.ietf.org/doc/html/rfc9113) — overview

## Key Concepts
- **Schema-first stubs:** `.proto` generates clients/servers — binary Protobuf payloads.
- **HTTP/2 multiplexing:** many RPCs on one TCP connection without head-of-line HTTP/1.1 churn.
- **Four call types:** unary, server streaming, client streaming, bidirectional.
- **Deadlines & metadata:** cancel long calls; metadata carries auth/tracing like headers.
- **Browser caveat:** browsers need grpc-web; native gRPC is primarily service-to-service.

## Technical Details
```
Service method call (generated stub)
        │
        ▼
Protobuf serialize
        │
        ▼
HTTP/2 frames (single TCP connection, multiplexed)
        │
        ▼
Server stub → handler
```

```protobuf
syntax = "proto3";
package demo;

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply);
  rpc Chat (stream ChatMessage) returns (stream ChatMessage);
}

message HelloRequest { string name = 1; }
message HelloReply   { string message = 1; }
```

| Type | Pattern |
|------|---------|
| Unary | Single request → single response |
| Server streaming | One request → stream of responses |
| Client streaming | Stream of requests → one response |
| Bidirectional | Both sides stream |

- **Metadata** — analogous to HTTP headers (auth tokens, tracing)
- **Context deadlines** — cancel long calls (`context.WithTimeout`)
- **Status codes** — `codes.NotFound`, `codes.DeadlineExceeded`
- **Load balancing** — L7 proxies need gRPC-aware balancing (HTTP/2 connection affinity)
- **mTLS** — common in service meshes (Istio, Linkerd)

## Real-World Applications
Microservice meshes, mobile backends that already speak Protobuf, and streaming APIs (logs, events) inside a cluster.

**Example:** A Go payment service exposes `Charge` as unary gRPC with a 200ms deadline; the mesh enforces mTLS and retries only idempotent codes.

## Pros/Cons or Trade-offs
- **Pro:** Strong contracts, efficient binary payloads, first-class streaming and deadlines.
- **Con:** Harder to curl/debug than JSON REST; public browser APIs often stay REST.
- **Con:** Naive L4 load balancing can pin poorly without HTTP/2 awareness.

## Comparison
| gRPC | REST/JSON |
|------|-----------|
| Binary, schema-first | Human-readable, flexible |
| HTTP/2 multiplexing | Often HTTP/1.1 per request |
| Browser support needs grpc-web | Native in browsers |

- vs [[webSocket]]: WebSocket is a generic full-duplex pipe; gRPC adds IDL, stubs, and status model.

## Mistakes to Avoid
- Exposing raw gRPC as a public browser API without grpc-web or a gateway.
- Ignoring deadlines — hung handlers cascade under load.
- Balancing gRPC like HTTP/1.1 round-robin without understanding connection reuse.
- Choosing gRPC for a public partner API that needs human-readable debugging and loose coupling.
