[[Firebase]]

# Multicast delivery

> One-line: what / why for **Multicast delivery** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#How multicast delivery work in FCM?]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

[`sendEachForMulticast(MulticastMessage message)`](https://firebase.google.com/docs/reference/admin/java/reference/com/google/firebase/messaging/FirebaseMessaging#sendEachForMulticast(com.google.firebase.messaging.MulticastMessage))
Multicast delivery in [[FCM Token (Firebase Cloud Messaging Token)]] refers to the ability to send a single message to multiple devices by providing multiple FCM registration tokens in one API call.
- this is useful for targeting a specific set to devices without creating a topic or group.

## Standard config / commands

…

## How multicast delivery work in FCM?

Input: You supply a list of device registration tokens (up to 500 tokens in one request)

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
