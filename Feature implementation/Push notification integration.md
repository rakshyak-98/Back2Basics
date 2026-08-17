[[Firebase messaging]] [[FCM Token (Firebase Cloud Messaging Token)]] [[android]]

# Push notification integration

> Wire device push across Apple Push Notification service and FCM — platform credentials on the server, device tokens from the client, permission UX in the app.





## Interview Relevance
Interviewers separate provider credentials (APNs key/cert, FCM service account), token storage, and permission prompts from “just call an SDK.”

## Sources
- [Apple — Sending notification requests](https://developer.apple.com/documentation/usernotifications) — overview
- [Firebase — Cloud Messaging](https://firebase.google.com/docs/cloud-messaging) — deep-dive

## Key Concepts
- **APNs:** Apple’s pipe for iOS; needs key/certificate + bundle id.
- **FCM:** Google’s pipe; often also relays to APNs for iOS when configured.
- **Device token / FCM token:** store per install; refresh and prune.
- **Permission:** OS prompt — explain value before asking.
- **Payloads:** notification vs data messages; background limits differ per OS.

## Technical Details
```txt
App asks permission → receives token → POST /devices
Backend → APNs and/or FCM → device
```

| Platform | Typical credential |
|----------|--------------------|
| iOS direct | APNs auth key (.p8) |
| Android | FCM / Google services |
| iOS via FCM | FCM + uploaded APNs key |

## Real-World Applications
Order status and chat pings: server event → fan-out to user tokens → prune dead tokens from provider errors.

**Example:** Android works, iOS silent — missing APNs key upload in Firebase or wrong bundle id.

## Pros/Cons or Trade-offs
- **Pro:** OS-level delivery and battery-aware scheduling.
- **Con:** Multi-platform credential matrix and opaque provider failures.

## Comparison
- vs polling: push is event-driven but permission-gated.
- vs [[Firebase messaging]]: this note is integration checklist; Firebase notes cover send APIs.

## Mistakes to Avoid
- Shipping without a token refresh path.
- Treating data-only messages the same on iOS/Android without testing force-quit behavior.
- Hardcoding provider keys in the mobile app.
