[[HTTP module]] [[TCP]] [[webSocket]]

# gRPC

> gRPC — RPC over HTTP/2 with Protocol Buffers: you define a `.proto` contract, generate stubs, and call methods like local functions.

## Mental model

**Say it in one breath:** Client and server share a Protobuf schema; the client calls `ReserveStock`; bytes ride HTTP/2 (multiplexed streams, binary framing) — not JSON REST by default.

```txt
.proto ──protoc──► stubs
                      │
Client stub ──HTTP/2──► Server stub ──► your handler (Context + codes)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **IDL / `.proto`** | Contract source of truth | “We version `package api.v1` and generate code.” |
| --- | --- | --- |
| **Unary / streaming** | 1:1 vs client/server/bidi streams | “Streaming is native; not bolted-on chunked HTTP.” |
| **Deadline** | Client timeout on the Context | “Deadlines propagate; I cancel downstream work.” |
| **Status codes** | gRPC codes, not HTTP 404 | “Map domain errors to `NotFound` / `InvalidArgument`.” |
| **Interceptor** | Middleware for auth/metrics | “Unary and stream interceptors wrap handlers.” |
| **Protobuf** | Compact binary encoding | “CPU on varints, not JSON string parsing.” |

### How the story goes

1. Write `.proto` service + messages; generate stubs.
2. Server implements generated interface; respects `ctx`.
3. Client dials (`dns:///`, TLS), sets deadline, calls RPC.
4. Errors return `status` + optional details — not ad-hoc strings only.

## Standard config / commands

```protobuf
syntax = "proto3";
package inventory.v1;
option go_package = "github.com/org/repo/internal/gen/inventory/v1";

service InventoryAPI {
  rpc ReserveStock(ReserveStockRequest) returns (ReserveStockResponse);
}

message ReserveStockRequest {
  string idempotency_key = 1;
  string sku = 2;
  int32 quantity = 3;
}
```

```go
// Server: honor cancellation
func (s *InventoryServer) ReserveStock(ctx context.Context, req *pb.ReserveStockRequest) (*pb.ReserveStockResponse, error) {
    if err := ctx.Err(); err != nil {
        return nil, status.Errorf(codes.Canceled, "client cancelled: %v", err)
    }
    // Pass ctx to DB so the gRPC deadline applies
    ...
}

// Interceptor: auth from metadata (HTTP/2 headers)
md, ok := metadata.FromIncomingContext(ctx)
```

```bash
# Reflection / debug
grpcurl -plaintext localhost:50051 list
grpcurl -d '{"sku":"ABC","quantity":1}' localhost:50051 inventory.v1.InventoryAPI/ReserveStock
```

| Knob | Why it matters |

| TLS + ALPN `h2` | Many LBs break HTTP/2 if misconfigured |
| --- | --- |
| Max message size | Default limits surprise large payloads |
| Keepalive | Dead peers and NAT timeouts on long streams |
| Deadline / retry policy | Without deadlines, hung RPCs pile up |

## Interface Definition (Protobuf IDL)

- **Version in package** — `api.v1` versus `api.v2`; don’t break wire fields (tag numbers).
- **Well-known types** — prefer `google.protobuf.Timestamp` / wrappers for nullability.
- **Errors** — `google.golang.org/grpc/status` + `errdetails` for field violations.

```go
st := status.New(codes.InvalidArgument, "invalid stock quantity")
st, _ = st.WithDetails(&errdetails.BadRequest{FieldViolations: []*errdetails.BadRequest_FieldViolation{{
    Field: "quantity", Description: "must be > 0",
}}})
return nil, st.Err()
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `Unavailable` / dial fail | DNS, port, TLS, HTTP/2 on LB | Fix target; enable h2; bypass broken proxy |
| `DeadlineExceeded` | Client timeout too tight / slow dep | Raise deadline; fix slow DB; check ctx propagation |
| `Canceled` storms | Client disconnect / retry loop | Stop work on `ctx.Done()`; fix client retries |
| `ResourceExhausted` | Message too big / quota | Raise limits; paginate; backpressure |
| Browser can’t call gRPC | Browsers need grpc-web | Use grpc-web proxy or JSON gateway |
| Version skew | Old stub vs new server | Compatible field adds; bump package on breaks |

## Gotchas

> [!WARNING]
> **Returning raw `error` or HTTP codes** — clients expect gRPC `status` codes; leaking `EOF` helps no one.

> [!WARNING]
> **Ignoring Context** — continuing DB work after client cancel wastes capacity and causes ghosts.

> [!WARNING]
> **Load balancers that only understand HTTP/1.1** — gRPC needs true HTTP/2 end-to-end (or a dedicated L7 that speaks h2).

> [!WARNING]
> **Protobuf field reuse** — changing type on the same tag number corrupts data silently.

## When NOT to use

- **Public browser APIs without a gateway** — prefer REST/JSON or GraphQL; add grpc-web only if you must.
- **Simple webhooks / human-debugged HTTP** — curl-friendly JSON wins for operations speed.
- **File download at CDN scale** — object storage + HTTPS, not unary RPCs of multi-GB blobs.

## Related

[[HTTP module]] [[TCP]] [[webSocket]] [[TLS (Transport Layer Security)]]
