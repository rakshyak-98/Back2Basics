[[Firebase]] [[Firebase messaging]]

# firebase reminders configuration

> Scheduled Firebase Cloud Functions query Firestore for upcoming events and send email reminders — combine `functions.pubsub.schedule`, Firestore range queries, and a mail transport (nodemailer or SendGrid).

---

## Scheduled reminder function

```sh
npm install firebase-admin firebase-functions nodemailer
```

```js
const functions = require('firebase-functions');
const admin = require('firebase-admin');
const nodemailer = require('nodemailer');

admin.initializeApp();

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.MAIL_USER,
    pass: process.env.MAIL_PASS, // use app password or OAuth — not raw password in code
  },
});

exports.sendClassReminders = functions.pubsub
  .schedule('every 5 minutes')
  .onRun(async () => {
    const now = new Date();
    const upcomingTime = new Date(now.getTime() + 30 * 60 * 1000);

    const snapshot = await admin.firestore().collection('classes')
      .where('startTime', '>=', now.toISOString())
      .where('startTime', '<=', upcomingTime.toISOString())
      .get();

    const emails = snapshot.docs.map(doc => ({
      to: doc.data().userEmail,
      subject: `Reminder: Your class '${doc.data().className}' starts soon!`,
      text: `Your class starts at ${doc.data().startTime}. Be ready!`,
    }));

    for (const mail of emails) {
      await transporter.sendMail(mail);
    }
  });
```

| Piece | Role |
|-------|------|
| `pubsub.schedule` | Cron-style trigger (every 5 minutes) |
| Firestore range query | Classes starting within next 30 minutes |
| `nodemailer` | SMTP delivery |

---

## Production hardening

- Store mail credentials in Firebase environment config or Secret Manager — not in source.
- Mark documents as `reminderSent` after send to avoid duplicate emails on the next cron tick.
- Composite index required for `startTime` range queries — deploy indexes from `firestore.indexes.json`.
- Consider push ([[Firebase messaging]]) instead of or alongside email for time-sensitive alerts.

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Duplicate reminders | No sent flag | Update doc after successful send |
| Function times out | Large batch | Paginate query; queue per-message |
| Query returns nothing | Wrong timestamp format | Align ISO strings vs Firestore `Timestamp` |
| Gmail blocks SMTP | Less secure app access | App password or transactional provider |

---

## Related

[[Firebase messaging]] · [[Firebase]]
