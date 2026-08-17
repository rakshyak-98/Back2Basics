[[HTTP module]] [[JWT authentication]] [[TLS (Transport Layer Security)]] [[MQTT]] [[kafka]] [[Web hooks]]

# Webhook

> Server-to-server HTTP callback when something happens — the receiver must verify, dedupe, and answer fast; it is not a durable message bus.

```txt
        Webhook ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about webhooks to test signature verification, idempotency u…

## Sources
- [Wikipedia — Webhook](https://en.wikipedia.org/wiki/Webhook) — overview
- [Stripe — Webhooks](https://stripe.com/docs/webhooks) — deep-dive
- [GitHub Docs — Validating webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries) — deep-dive

## Key Concepts
- **Push vs poll:** lower latency than polling
- **Signature verification:** HMAC over the *raw* body with a shared secret → reject unsigned or tampered p…
- **Idempotency:** store `event.id` / delivery id before side effects → retries must not double-…
- **Fast ACK, async work:** return 2xx within the publisher timeout after durable enqueue → long work bel…
- **Not a bus:** no global ordering, limited backlog, weak fan-out


- **Core:** A webhook is an HTTP POST (usually JSON) from a publisher to your public HTTP…

## Technical Details
```
Publisher                    Your service
    │  POST /hooks/stripe     │
    │  Signature: …           │
    ├────────────────────────►│ verify → enqueue → 200 OK (< timeout)
    │                         └── worker processes job
    │  retry on 5xx/timeout   │
```

### Minimal verified receiver (Express + raw body)

```javascript
const express = require('express');
const crypto = require('crypto');

app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  if (await alreadyProcessed(event.id)) {
    return res.json({ received: true });
  }

  await enqueueJob('stripe-event', event);
  await markProcessed(event.id);
  res.json({ received: true });
});
```

### Generic HMAC pattern

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

### Local tunnel / replay

```shell
ngrok http 3000
# or: cloudflared tunnel --url http://localhost:3000

curl -i -X POST https://api.example.com/webhooks/github \
  -H 'Content-Type: application/json' \
  -H 'X-Hub-Signature-256: sha256=…' \
  -d @payload.json
```

- **Production checklist:** HTTPS only

| Symptom | Check | Fix |
|---------|-------|-----|
| No events | Publisher delivery log | URL, DNS, firewall, expired tunnel |
| 401/403 / invalid signature | Secret or body parsing | Raw body before JSON parser; matching secret |
| Duplicate side effects | Same `event.id` twice | Idempotency store (unique constraint) |
| Publisher stopped retrying | 4xx on transient failure | 5xx only when you want retry |
| Timeouts in publisher log | Handler too slow | Enqueue then 200 |
| Out-of-order events | Distributed delivery | Version fields per aggregate |

## Mistakes to Avoid
- **Mistake:** Returning 200 before the event is durably enqueued
- **Mistake:** Skipping signature checks because the URL is “secret.”
- **Mistake:** Disabling verification in staging and forgetting to re-enable it

## Pros/Cons or Trade-offs
- **Pro:** Near-real-time, simple HTTP, no always-on poller.
- **Con:** You must expose and harden a public endpoint; retries create duplicates without idempotency.
- **Con:** Poor fit for high-volume internal fan-out compared with a log/queue.

## Comparison
- vs polling: webhooks push; polling is simpler operationally but slower and chatty.
- vs [[SSE (Server-Sent Events)]]: SSE pushes to *browsers* over one long HTTP response
- vs [[kafka]]: Kafka is a durable internal log; webhooks are external integration glue.
- Alias stub: [[Web hooks]] redirects here.


### Use cases
- Stripe payment events, GitHub repository events, Slack interactivity, and Saa…

- **Example:** Stripe sends `invoice.paid`
