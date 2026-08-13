<!-- note-strategy: operational -->
[[NodeJS]] [[Transporter in Email sending]] [[Protocol/gRPC]] [[Protocol/MQTT]] [[HTTP module]]

# Transporters

> Pluggable send/receive layer — business code calls `send`/`emit`; the transporter owns HTTP, gRPC, MQTT, broker details.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Swap the wire without rewriting domain logic — same interface over different protocols (HTTP, AMQP, NATS, MQTT, gRPC).

```txt
Service ──transporter.send──► HTTP | gRPC | MQTT | broker
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Transporter** | I/O adapter | “Decouple protocol from business.” |
| **Broker vs RPC** | Async bus vs request/reply | “Pick semantics, not just speed.” |
| **Email transporter** | Nodemailer SMTP/API | “See [[Transporter in Email sending]].” |

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Works on HTTP, fails on bus | Ack/retry semantics | Make handlers idempotent |
| Backpressure | Unbounded queue | Limit in-flight; drop/slow |
| Dual writes | Two transporters | Outbox / single writer |
| Auth mismatch | Per-protocol creds | Centralize secrets in config |

---

## Gotchas

> [!WARNING]
> **Protocol leak** — if domain imports MQTT types, you didn’t abstract.

> [!WARNING]
> **At-least-once delivery** — duplicates happen; design for them.

---

## When NOT to use

- **One protocol forever** — direct client may be simpler.
- **Ultra-low latency peer path** — specialized stacks (e.g. raw sockets) without a bus.

---

## Related

[[Transporter in Email sending]] [[Protocol/gRPC]] [[MQTT]] [[Message Broker]] [[HTTP module]]
