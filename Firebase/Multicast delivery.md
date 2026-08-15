[[FCM Token (Firebase Cloud Messaging Token)]] [[Firebase messaging]]

# Multicast delivery

> FCM multicast sends one payload to up to 500 registration tokens in one Admin SDK call — best for an explicit device list without a topic.

## Interview Relevance

Interviewers want the 500 limit, `sendEachForMulticast` per-token results, and chunking/pruning strategy.

## Sources

- [Firebase — Send a message to multiple devices](https://firebase.google.com/docs/cloud-messaging/send-message#send-messages-to-multiple-devices) — deep-dive

## Key Concepts

- **Explicit set:** you pass tokens; not “everyone subscribed to X.”
- **500 cap per call:** larger audiences need a loop.
- **Per-token results:** success/failure array aligns with input order.
- **Topics alternative:** better for true broadcast subscribe models.

## Technical Details

```js
const batchResponse = await admin.messaging().sendEachForMulticast({
  notification: { title: "Update", body: "New content available" },
  tokens: tokenArray, // max 500
});
batchResponse.responses.forEach((resp, idx) => {
  if (!resp.success) {
    // delete stale tokenArray[idx] when not-registered
  }
});
```

| Limit | Value |
|-------|-------|
| Tokens per multicast | 500 |
| Payload | Normal FCM message limits |

## Real-World Applications

Notify all devices for one account (often <<500) in a single multicast; for all-user blasts, prefer topics or chunked jobs.

**Example:** High failure rate after app reinstall wave — prune `registration-token-not-registered` aggressively.

## Pros/Cons or Trade-offs

- **Pro:** Simple API for known token lists; detailed failures.
- **Con:** Not a substitute for topic fan-out at huge scale.

## Comparison

- vs topic send: topics scale broadcast; multicast targets a concrete list.
- vs single send: multicast reduces HTTP chatter for batches ≤500.

## Mistakes to Avoid

- Passing >500 tokens and assuming the SDK silently handles it.
- Ignoring `failureCount` / per-token errors.
- Deduping poorly so retries double-notify users.
