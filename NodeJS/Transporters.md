[[NodeJS]] [[Transporter in Email sending]] [[Protocol/gRPC]] [[Protocol/MQTT]] [[HTTP module]] [[MQTT]] [[Message Broker]]

# Transporters

> Pluggable send/receive layer — business code calls `send`/`emit`; the transporter owns HTTP, gRPC, MQTT, broker details.

```txt
        Transporters ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **Transporters** to check whether you can explain the mechan…

## Sources
- [Wikipedia — Transporters](https://en.wikipedia.org/wiki/Transporters) — overview

## Key Concepts
- **Transporter:** I/O adapter — Decouple protocol from business.
- **Broker vs RPC:** Async bus vs request/reply — Pick semantics, not just speed.
- **Email transporter:** Nodemailer SMTP/API — See [[Transporter in Email sending]].

## Technical Details
```txt
Service ──transporter.send──► HTTP | gRPC | MQTT | broker
```

```js
// Pattern — interface, many backends
export function createTransporter(kind, opts) {
  if (kind === 'http') return httpTransport(opts)
  if (kind === 'nats') return natsTransport(opts)
  throw new Error(`unknown transporter: ${kind}`)
}

await transporter.send({ type: 'order.created', payload })
```

| Knob | Why it matters |
|------|----------------|
| Timeouts / retries | Don’t hang callers |
| Serialization | JSON vs protobuf |
| Idempotency keys | At-least-once buses |

## Mistakes to Avoid
- **Mistake:** **Protocol leak**
- **Mistake:** **At-least-once delivery** — duplicates happen; design for them
- **Mistake:** **Works on HTTP, fails on bus:** check Ack/retry semantics
- **Mistake:** **Backpressure:** check Unbounded queue
- **Mistake:** **Dual writes:** check Two transporters
- **Mistake:** **Auth mismatch:** check Per-protocol creds

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Pluggable send/receive layer — business code calls `send`/`emit`; the transporte…).
- **Con / when not:** **One protocol forever** — direct client may be simpler.
- **Con / when not:** **Ultra-low latency peer path**

## Comparison
- vs [[Transporter in Email sending]]: know when each applies


### Use cases
- In production APIs and tooling, **Transporters** shows up whenever teams ship…
