[[FCM Token (Firebase Cloud Messaging Token)]] [[Multicast delivery]]

# Firebase messaging

> Admin SDK / HTTP v1 sends pushes through FCM — single token, multicast (≤500), topics, or a fan-out job for large audiences.

```txt
        Firebase messaging ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers catch the classic bug: `tokens.slice(0, 500)` once

## Sources
- [Firebase Admin — Send messages](https://firebase.google.com/docs/cloud-messaging/send-message) — deep-dive
- [Firebase — MulticastMessage](https://firebase.google.com/docs/reference/admin/node/firebase-admin.messaging.multicastmessage) — overview

## Key Concepts
- **Single token:** one device.
- **Multicast:** up to 500 tokens per call → chunk larger lists.
- **Topics / conditions:** broadcast to subscribers.
- **Fan-out job:** thousands of tokens — chunk and parallelize with backoff.

## Technical Details
```txt
Token list → chunk(500) → sendEachForMulticast → handle per-token errors
```

```js
const response = await admin.messaging().sendEachForMulticast({
  notification: { title: "Hello", body: "World" },
  tokens: deviceTokens.slice(offset, offset + 500),
});
// Inspect response.responses; prune not-registered
```

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Partial audience | Only first 500 sent | Loop chunks with offset |
| Retry storms | No backoff | Cap retries; circuit break |
| Duplicate notifies | Unsafe retries | Idempotent send keys |

## Mistakes to Avoid
- **Mistake:** Dropping tokens beyond the first chunk
- **Mistake:** Retrying forever on permanent token errors
- **Mistake:** Mixing notification payload expectations across platforms withou…

## Pros/Cons or Trade-offs
- **Pro:** Managed delivery across iOS/Android/Web.
- **Con:** Application-level fan-out and hygiene still your job.

## Comparison
- vs [[Multicast delivery]]: messaging note covers patterns
- vs email/SMS: push is device-permissioned and token-based.


### Use cases
- Campaign worker reads user tokens, chunks by 500, sends, deletes dead tokens,…

- **Example:** 2,000 tokens with a single `slice(0, 500)`
