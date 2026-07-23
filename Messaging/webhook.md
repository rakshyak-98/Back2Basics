[[HTTP module]] [[JWT authentication]] [[TLS (Transport Layer Security)]]

# Webhook

> One-line: server-to-server HTTP callback on events — receiver must verify, dedupe, and respond fast — **not** a reliable message bus.

## Mental model

Publisher (Stripe, GitHub, Slack) POSTs an event payload to your HTTPS URL when something happens. Delivery is **best-effort** with retries — your endpoint must be **idempotent** and **quick** (ack, then process async).

```
Publisher                    Your service
    │  POST /hooks/stripe     │
    │  Signature: ...         │
    ├────────────────────────►│ verify → enqueue → 200 OK (< 5s)
    │                         └── worker processes job
    │  retry on 5xx/timeout   │
    ◄─────────────────────────┤ (exponential backoff, hours)
```

Contrasts with polling: lower latency, higher ops burden (public URL, signature crypto, replay handling).

## Standard config / commands

### Minimal verified receiver (Express + raw body)

```javascript
const express = require('express');
const crypto = require('crypto');

const app = express();

// Raw body required for HMAC verification — before json parser
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Idempotency: skip if event.id already processed
  if (await alreadyProcessed(event.id)) {
    return res.json({ received: true });
  }

  await enqueueJob('stripe-event', event);   // async — don't block response
  await markProcessed(event.id);
  res.json({ received: true });
});
```

### Generic HMAC verification pattern

```javascript
function verifyHmac(rawBody, signatureHeader, secret) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
    .digest('hex');
  const provided = signatureHeader.replace(/^sha256=/, '');
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(provided));
}
```

### Local development tunnel

```shell
# Expose localhost to publisher (dev only)
ngrok http 3000
# or cloudflared tunnel --url http://localhost:3000

# Manual replay for debug
curl -i -X POST https://api.example.com/webhooks/github \
  -H 'Content-Type: application/json' \
  -H 'X-Hub-Signature-256: sha256=...' \
  -d @payload.json
```

### Production checklist

- [ ] HTTPS only; valid cert
- [ ] Verify signature (**every** request — no exceptions)
- [ ] Constant-time compare for HMAC
- [ ] Idempotency key (`event.id`, `X-GitHub-Delivery`, `Idempotency-Key`)
- [ ] Respond **2xx within provider timeout** (often 5–30s)
- [ ] Process async (queue/worker)
- [ ] Log delivery ID, not full secrets
- [ ] Rotate webhook secrets; support dual-secret during rotation
- [ ] Rate limit / IP allowlist if provider publishes egress CIDRs

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No events arriving | Publisher dashboard delivery log | URL wrong; tunnel expired; DNS/firewall |
| All return 401/403 | Signature secret mismatch | Update secret; ensure raw body for HMAC |
| `400 invalid signature` | JSON parser ran before verify | Use `express.raw()` on webhook route only |
| Duplicate side effects | Same `event.id` processed twice | Idempotency store (Redis/DB unique constraint) |
| Publisher stopped retrying | Returned 4xx on transient error | Return 5xx only when you want retry; 2xx if ignored intentionally |
| Timeouts in publisher log | Handler > 30s | Move work to queue; return 200 immediately |
| Works in staging, not prod | Different secret / URL | Separate endpoints per env |
| SSL errors on receive | Cert chain, TLS version | Fix cert; use provider-minimum TLS |
| Out-of-order events | Normal for distributed systems | Design for ordering per aggregate; use version fields |

## Gotchas

> [!WARNING]
> **Return 200 only after durable enqueue** — if you 200 then crash before queue write, event is lost forever (publisher won't retry).

> [!WARNING]
> **Never expose webhook routes without auth** — obscurity URLs get scanned. Signature verification is mandatory.

- **Replay attacks:** include timestamp tolerance (Stripe `t=` prefix) or nonce store for custom HMAC.
- **GitHub:** `X-Hub-Signature-256` on raw body; `application/json` vs `application/x-www-form-urlencoded` for some hooks.
- **Load balancer idle timeout** < long processing → LB 504 while worker still runs — async pattern fixes this.
- **Testing:** use provider CLI (`stripe listen --forward-to`) instead of disabling verification.

## When NOT to use

- High-volume internal events → message queue ([[MQTT]], Kafka, SQS) with at-least-once semantics.
- Client browser callbacks → CORS + user session; webhooks are server-to-server.
- Need guaranteed ordering globally → webhook + retry isn't enough; use ordered stream.

## Related

[[HTTP module]] · [[JWT authentication]] · [[TLS (Transport Layer Security)]] · [[Web hooks]]
