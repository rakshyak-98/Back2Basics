[[FCM Token (Firebase Cloud Messaging Token)]] [[Multicast delivery]]

# Firebase messaging

> Admin SDK / HTTP v1 sends pushes through FCM — single token, multicast (≤500), topics, or a fan-out job for large audiences.





## Interview Relevance
Interviewers catch the classic bug: `tokens.slice(0, 500)` once — and they want per-token failure handling plus safe retries.

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

## Real-World Applications
Campaign worker reads user tokens, chunks by 500, sends, deletes dead tokens, logs `failureCount`.

**Example:** 2,000 tokens with a single `slice(0, 500)` — 1,500 users silently skipped.

## Pros/Cons or Trade-offs
- **Pro:** Managed delivery across iOS/Android/Web.
- **Con:** Application-level fan-out and hygiene still your job.

## Comparison
- vs [[Multicast delivery]]: messaging note covers patterns; multicast note details the 500-token API.
- vs email/SMS: push is device-permissioned and token-based.

## Mistakes to Avoid
- Dropping tokens beyond the first chunk.
- Retrying forever on permanent token errors.
- Mixing notification payload expectations across platforms without testing.
