[[Firebase messaging]] [[FCM Token (Firebase Cloud Messaging Token)]]

# Firebase reminders configuration

> Scheduled Cloud Functions query Firestore for upcoming events and send reminders — cron trigger + range query + mail/push transport.

## Interview Relevance

Interviewers check idempotent schedules (do not email twice), secret handling for SMTP, and Firestore query constraints on the time window.

## Sources

- [Firebase — Schedule functions](https://firebase.google.com/docs/functions/schedule-functions) — deep-dive
- [Firestore — Query data](https://firebase.google.com/docs/firestore/query-data/queries) — overview

## Key Concepts

- **Scheduler:** `pubsub.schedule` (or Cloud Scheduler) → run every N minutes.
- **Window query:** `startTime` between now and now+δ → candidates for reminder.
- **Transport:** email (nodemailer/SendGrid) and/or FCM push.
- **Idempotency:** mark `reminderSentAt` so overlaps do not double-send.

## Technical Details

```js
exports.sendClassReminders = functions.pubsub
  .schedule("every 5 minutes")
  .onRun(async () => {
    const now = new Date();
    const upcoming = new Date(now.getTime() + 30 * 60 * 1000);
    const snapshot = await admin.firestore().collection("classes")
      .where("startTime", ">=", now.toISOString())
      .where("startTime", "<=", upcoming.toISOString())
      .where("reminderSent", "==", false)
      .get();
    // send mail/push; then set reminderSent=true in a transaction/batch
  });
```

Keep `MAIL_USER` / API keys in environment config — never hardcode app passwords in source.

## Real-World Applications

Class or appointment products: remind 30 minutes before start via email and optional push.

**Example:** Function runs every 5 minutes with a 30-minute window — without a sent flag, users get duplicate reminders on every tick.

## Pros/Cons or Trade-offs

- **Pro:** Serverless scheduler + Firestore is quick to ship.
- **Con:** Hot schedules need indexes, idempotency, and rate limits on the mail provider.

## Comparison

- vs client-side local notifications: server reminders work across devices; require trustworthy clocks and data.
- vs [[Firebase messaging]]: this note is the scheduling pattern; messaging is the push send path.

## Mistakes to Avoid

- No “already sent” marker on overlapping schedule windows.
- Storing Gmail passwords in the repository.
- Unbounded queries without composite indexes for the filter set.
