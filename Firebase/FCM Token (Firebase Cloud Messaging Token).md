[[Messaging/webhook]] [[android/sdkmanager]] [[Security/Token rotation]]

# FCM token (Firebase Cloud Messaging)

> Device-scoped token identifying one app install for push delivery — rotate on reinstall, clear data, or token refresh.

## Mental model

Client SDK asks FCM for a registration token. Your backend stores `(userId, fcmToken, platform)`. FCM uses token + Firebase project credentials to deliver to Google/Apple push infrastructure. Tokens **expire and refresh** — listen for refresh callbacks and update DB.

```
App → FCM SDK → token → your API → store
Server → FCM HTTP v1 → device
```

## Standard config / commands

### Client (conceptual)

```js
// Web — firebase.messaging()
const token = await getToken(messaging, { vapidKey: VAPID_KEY });
// Send token to backend on login + onTokenRefresh
```

### Server send (HTTP v1)

```bash
# OAuth2 access token from service account
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

### Backend storage

| Field | Purpose |
|-------|---------|
| `user_id` | Target user |
| `token` | FCM device token (unique per app instance) |
| `platform` | ios / android / web |
| `updated_at` | Stale token cleanup |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `registration-token-not-registered` | Stale token in DB | Delete token; client re-registers |
| Web push fails | VAPID key, HTTPS | Serve over HTTPS; matching VAPID in Firebase console |
| iOS no push | APNs key/certs in Firebase | Upload APNs auth key; enable push capability |
| Duplicate notifications | Multiple tokens per user | Dedupe; send to latest token set |
| Works on Android, not iOS | Permission / focus mode | Request permission; check provisional auth |

## Gotchas

> [!WARNING]
> **Legacy server key API deprecated** — migrate to HTTP v1 + service account.
>
> **Don't use token as user id** — one user, many devices; many tokens.
>
> **Test tokens in logs** — treat as secrets in support tickets.

## When NOT to use

- Don't poll FCM for inbound messages — use onMessage handlers + your API for data sync.
- Don't store tokens without TTL cleanup — unregistered errors will clutter sends.

## Related

[[Messaging/webhook]] [[Security/Token rotation]] [[Protocol/MQTT]]
