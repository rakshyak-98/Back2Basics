[[Feature implementation]] [[Firebase messaging]] [[FCM Token (Firebase Cloud Messaging Token)]] [[Firebase]]

# Push notification integration

> Push notifications require platform-specific credentials — Apple Push Notification service (APNs) for iOS, Firebase Cloud Messaging (FCM) for Android and web — your backend authenticates to the push gateway, not directly to the device.

---

## Platform credentials

| Platform | Credential | Purpose |
|----------|------------|---------|
| iOS | APNs auth key or certificate | Proves your server may send for your app bundle ID |
| Android / web | FCM service account (HTTP v1) | OAuth token for `fcm.googleapis.com` |
| Web push | VAPID key pair | Browser subscription endpoint |

APNs certificate or auth key proves to Apple that your backend is authorized to deliver notifications for your application. Without valid credentials, Apple does not deliver pushes.

---

## End-to-end flow

```txt
App registers → device token → your API stores (userId, token, platform)
Event occurs → your server → FCM or APNs → device OS → notification UI
```

Store tokens per device install, not per user — one user may have many tokens. Listen for token refresh and delete stale tokens on `registration-token-not-registered` errors.

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| iOS never receives | Missing APNs key in Firebase or Xcode capability | Upload key; enable Push Notifications |
| Android works, iOS fails | Separate credential paths | Verify APNs + FCM project link |
| Duplicate notifications | Multiple tokens per user | Send to latest token set; dedupe |
| Web push fails | Not HTTPS or wrong VAPID | HTTPS only; match VAPID in console |

Do not use the device token as the user identifier. Treat tokens as secrets in logs and support tickets.

---

## Related

[[FCM Token (Firebase Cloud Messaging Token)]] · [[Firebase messaging]] · [[Multicast delivery]]
