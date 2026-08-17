[[NodeJS]] [[Transporter in Email sending]] [[Protocol/gRPC]] [[Protocol/MQTT]] [[HTTP module]] [[MQTT]] [[Message Broker]]

# Transporters

> Pluggable send/receive layer — business code calls `send`/`emit`; the transporter owns HTTP, gRPC, MQTT, broker details.





## Interview Relevance
Interviewers use **Transporters** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Transporter**, **Broker vs RPC**, **Email transporter**.

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

## Real-World Applications
In production APIs and tooling, **Transporters** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Protocol leak** — if domain imports MQTT types, you didn’t abstract; **At-least-once delivery** — duplicates happen; design for them.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Pluggable send/receive layer — business code calls `send`/`emit`; the transporte…).
- **Con / when not:** **One protocol forever** — direct client may be simpler.
- **Con / when not:** **Ultra-low latency peer path** — specialized stacks (e.g. raw sockets) without a bus.

## Comparison
vs [[Transporter in Email sending]]: know when each applies — do not treat them as interchangeable. vs [[Protocol/gRPC]]: know when each applies — do not treat them as interchangeable. vs [[Protocol/MQTT]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Protocol leak** — if domain imports MQTT types, you didn’t abstract.
- **At-least-once delivery** — duplicates happen; design for them.
- **Works on HTTP, fails on bus:** check Ack/retry semantics; fix: Make handlers idempotent
- **Backpressure:** check Unbounded queue; fix: Limit in-flight; drop/slow
- **Dual writes:** check Two transporters; fix: Outbox / single writer
- **Auth mismatch:** check Per-protocol creds; fix: Centralize secrets in config
