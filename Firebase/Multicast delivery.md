<!-- note-strategy: operational -->
[[Firebase]]

# Multicast delivery

> Multicast delivery — in FCM Token (Firebase Cloud Messaging Token) refers to the ability to send a single message to multiple devices by providing multiple…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Multicast delivery — in FCM Token (Firebase Cloud Messaging Token) refers to the ability to send a single message to multiple devices by providing multiple…

[`sendEachForMulticast(MulticastMessage message)`](https://firebase.google.com/docs/reference/administrator/java/reference/com/google/firebase/messaging/FirebaseMessaging#sendEachForMulticast(com.google.firebase.messaging.MulticastMessage))
Multicast delivery in [[FCM Token (Firebase Cloud Messaging Token)]] refers to the ability to send a single message to multiple devices by providing multiple FCM registration tokens in one API call.
- this is useful for targeting a specific set to devices without creating a topic or group.


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[Firebase]]
