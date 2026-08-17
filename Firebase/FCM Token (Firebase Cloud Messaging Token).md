[[Firebase messaging]] [[Multicast delivery]] [[Messaging/webhook]] [[android/sdkmanager]] [[Security/Token rotation]]

# FCM Token (Firebase Cloud Messaging Token)

> Registration token for one app install on one device — your backend stores it to target push; it rotates on reinstall, clear-data, and refresh callbacks.

```txt
        FCM Token (Firebas ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want token lifecycle (store, refresh, delete on `not-registered`…

## Sources
- [Firebase — About FCM messages](https://firebase.google.com/docs/cloud-messaging/concept-options) — overview
- [Firebase — HTTP v1 API](https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages) — deep-dive

## Key Concepts
- **One token ≈ one app instance:** not “one user forever.”
- **Refresh callbacks:** update DB when the SDK rotates the token.
- **Prune hard failures:** delete tokens returning `registration-token-not-registered`.
- **Auth to FCM:** OAuth access token from a Firebase service account (HTTP v1).

## Technical Details
```txt
App → FCM SDK → token → your API → database
Server → FCM HTTP v1 → Google/Apple push infra → device
```

```js
const token = await getToken(messaging, { vapidKey: VAPID_KEY });
// POST token to backend on login and on every refresh
```

| Field | Purpose |
|-------|---------|
| `user_id` | Target user |
| `token` | FCM device token |
| `platform` | ios / android / web |
| `updated_at` | Stale cleanup |

## Mistakes to Avoid
- **Mistake:** Treating a token as a permanent user id
- **Mistake:** Still using deprecated legacy server keys for new work
- **Mistake:** Ignoring refresh events until sends start failing in production

## Pros/Cons or Trade-offs
- **Pro:** Precise device targeting without building your own push pipe.
- **Con:** Token churn requires disciplined DB hygiene.

## Comparison
- vs topics: tokens target explicit devices; topics broadcast to subscribers.
- vs [[Multicast delivery]]: token is the address; multicast is how you send to many addresses.


### Use cases
- Multi-device users: store many tokens per user

- **Example:** User reinstalls the app
