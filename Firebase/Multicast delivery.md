[[Firebase]]

# Multicast delivery

> Multicast delivery — in FCM Token (Firebase Cloud Messaging Token) refers to the ability to send a single message to multiple devices by providing multiple…

## Mental model

**Say it in one breath:** Multicast delivery — in FCM Token (Firebase Cloud Messaging Token) refers to the ability to send a single message to multiple devices by providing multiple…

[`sendEachForMulticast(MulticastMessage message)`](https://firebase.google.com/docs/reference/administrator/java/reference/com/google/firebase/messaging/FirebaseMessaging#sendEachForMulticast(com.google.firebase.messaging.MulticastMessage))
Multicast delivery in [[FCM Token (Firebase Cloud Messaging Token)]] refers to the ability to send a single message to multiple devices by providing multiple FCM registration tokens in one API call.
- this is useful for targeting a specific set to devices without creating a topic or group.

## Related

[[Firebase]]
