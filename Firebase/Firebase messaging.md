[[Firebase]] [[FCM Token (Firebase Cloud Messaging Token)]] [[Multicast delivery]]

# Firebase messaging

> Firebase Admin SDK messaging sends push notifications via FCM HTTP v1 — batch APIs cap at 500 tokens per multicast call; larger audiences require chunking, topic subscriptions, or fanout jobs.

---

## Send patterns

| Pattern | When to use |
|---------|-------------|
| Single `token` | One device |
| [[Multicast delivery]] | Up to 500 tokens in one call |
| Topic `condition` | Broadcast to subscribers |
| Fanout job | Thousands of tokens — chunk and parallelize |

```txt
Token list → chunk(500) → sendEachForMulticast per chunk → handle per-token errors
```

A common logic flaw: `tokens.slice(0, 500)` sends to the first 500 only — tokens beyond 500 are silently dropped unless you loop chunks.

---

## Admin SDK (Node)

```js
const message = {
  notification: { title: 'Hello', body: 'World' },
  tokens: deviceTokens.slice(0, 500), // chunk larger lists
};
const response = await admin.messaging().sendEachForMulticast(message);
// Inspect response.responses for per-token failures
```

Remove failed tokens (`registration-token-not-registered`) from your database on each batch.

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Partial audience receives | Only first 500 tokens sent | Chunk with offset loop |
| Retry storm on failures | No backoff | Cap retries; circuit break |
| Duplicate side effects | Unsafe retries | Idempotent handlers; dedupe keys |
| Silent drops | Unhandled batch errors | Log `response.failureCount` |

Make retries safe — duplicate notification sends annoy users and may violate compliance.

---

## Related

[[FCM Token (Firebase Cloud Messaging Token)]] · [[Multicast delivery]]

## Sources

- [Firebase MulticastMessage](https://firebase.google.com/docs/reference/admin/java/reference/com/google/firebase/messaging/MulticastMessage)
