[[HTTP module]] · [[TCP]] · [[TLS (Transport Layer Security)]] · [[webSocket]]

# gRPC

> gRPC is a high-performance RPC framework over HTTP/2 with Protocol Buffers payloads — strong typing, streaming, and deadlines make it the default for service-to-service calls in many microservice stacks.

---

## Stack

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

Specification at [grpc.io](https://grpc.io/docs/what-is-grpc/introduction/); HTTP/2 per [RFC 9113](https://datatracker.ietf.org/doc/html/rfc9113).

## Service definition

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

`protoc` generates client/server code in Go, Java, C++, Python, etc.

## Call types

| Type | Pattern |
|------|---------|
| Unary | Single request → single response |
| Server streaming | One request → stream of responses |
| Client streaming | Stream of requests → one response |
| Bidirectional | Both sides stream |

## Metadata and deadlines

- **Metadata** — analogous to HTTP headers (auth tokens, tracing)
- **Context deadlines** — cancel long calls (`context.WithTimeout`)
- **Status codes** — `codes.NotFound`, `codes.DeadlineExceeded`

## Load balancing and TLS

- L7 proxies need **gRPC-aware** balancing (HTTP/2 connection affinity)
- **mTLS** common in service meshes (Istio, Linkerd)

## vs REST ([[HTTP module]])

| gRPC | REST/JSON |
|------|-----------|
| Binary, schema-first | Human-readable, flexible |
| HTTP/2 multiplexing | Often HTTP/1.1 per request |
| Browser support needs grpc-web | Native in browsers |

## Recall

- Why does HTTP/2 help gRPC latency on a single connection?
- When would you choose REST over gRPC for a public API?

## Sources

- [gRPC documentation](https://grpc.io/docs/)
- [Protocol Buffers Language Guide](https://protobuf.dev/programming-guides/proto3/)
- [RFC 9113 — HTTP/2](https://datatracker.ietf.org/doc/html/rfc9113)
