[[Firebase]] [[Firebase messaging]] [[Multicast delivery]] [[Messaging/webhook]] [[android/sdkmanager]] [[Security/Token rotation]]

# FCM Token (Firebase Cloud Messaging Token)

> A Firebase Cloud Messaging (FCM) registration token identifies one app install on one device — your backend stores it to target push delivery; tokens rotate on reinstall, clear data, or refresh callbacks.

---

## Lifecycle

```txt
App → FCM SDK → registration token → your API → database
Server → FCM HTTP v1 (OAuth) → Google/Apple push infra → device
```

Client SDK requests a token. Your backend stores `(userId, fcmToken, platform, updated_at)`. FCM uses the token plus project credentials to route the message.

Tokens **expire and refresh** — register `onTokenRefresh` (or equivalent) and update the database. Delete tokens that return `registration-token-not-registered`.

---

## Client (conceptual)

```js
const token = await getToken(messaging, { vapidKey: VAPID_KEY });
// Send token to backend on login and on every refresh
```

---

## Server send (HTTP v1)

```bash
curl -X POST \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  https://fcm.googleapis.com/v1/projects/PROJECT_ID/messages:send \
  -d '{
    "message": {
      "token": "DEVICE_FCM_TOKEN",
      "notification": { "title": "Hi", "body": "Message" }
    }
  }'
```

Access token comes from a Firebase service account (not the deprecated legacy server key).

### Storage schema

| Field | Purpose |
|-------|---------|
| `user_id` | Target user |
| `token` | FCM device token (unique per app instance) |
| `platform` | `ios` / `android` / `web` |
| `updated_at` | Stale token cleanup |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `registration-token-not-registered` | Stale token in database | Delete; client re-registers |
| Web push fails | VAPID or HTTPS | HTTPS only; matching VAPID in console |
| iOS no push | APNs not linked | Upload APNs auth key; enable capability |
| Duplicate notifications | Multiple tokens per user | Dedupe; send to current set |

One user, many devices — never use the token as the user ID. Migrate off legacy server key API to HTTP v1.

---

## Related

[[Firebase messaging]] · [[Multicast delivery]] · [[Security/Token rotation]] · [[Messaging/webhook]]

## Sources

- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
