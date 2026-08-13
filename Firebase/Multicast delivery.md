[[Firebase]] [[FCM Token (Firebase Cloud Messaging Token)]] [[Firebase messaging]]

# Multicast delivery

> FCM multicast sends one message payload to up to 500 registration tokens in a single API call — use `sendEachForMulticast` when you have a specific device list without creating a topic or device group.

---

## When multicast fits

```txt
Known token list (≤500 per call) → MulticastMessage → per-token success/failure
```

Multicast targets a explicit set of devices. For broadcast to all subscribers, use **topics**. For very large lists, chunk tokens and call multicast repeatedly.

[`sendEachForMulticast`](https://firebase.google.com/docs/reference/admin/java/reference/com/google/firebase/messaging/FirebaseMessaging#sendEachForMulticast(com.google.firebase.messaging.MulticastMessage)) returns per-token results — unlike legacy multicast that hid individual failures.

---

## Example

```js
const message = {
  notification: { title: 'Update', body: 'New content available' },
  tokens: tokenArray, // max 500
};
const batchResponse = await admin.messaging().sendEachForMulticast(message);

batchResponse.responses.forEach((resp, idx) => {
  if (!resp.success) {
    const failedToken = tokenArray[idx];
    // Delete stale tokens; log others
  }
});
```

| Limit | Value |
|-------|-------|
| Tokens per multicast | 500 |
| Payload size | FCM message limits apply |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Only first N devices get message | No chunking loop | Split `tokens` into 500-size batches |
| High failure rate | Stale tokens | Prune on `registration-token-not-registered` |
| Duplicate notifications | Retries without idempotency | Track send IDs; safe retry policy |

---

## Related

[[FCM Token (Firebase Cloud Messaging Token)]] · [[Firebase messaging]]

## Sources

- [sendEachForMulticast](https://firebase.google.com/docs/reference/admin/java/reference/com/google/firebase/messaging/FirebaseMessaging#sendEachForMulticast(com.google.firebase.messaging.MulticastMessage))
