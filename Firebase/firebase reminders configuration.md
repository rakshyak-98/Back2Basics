[[Firebase]]

# firebase reminders configuration

> firebase reminders configuration — exports.sendClassReminders = functions.pubsub.schedule("every 5 minutes").onRun(async () => {

---

## Mental model

**Say it in one breath:** firebase reminders configuration — plain job, how I run it, how I know it’s broken.


```sh
npm install firebase-admin firebase-functions nodemailer
```
```js
const functions = require("firebase-functions");
const admin = require("firebase-admin");
const nodemailer = require("nodemailer");
admin.initializeApp();
const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "your-email@gmail.com",
    pass: "your-email-password",
  },
});
exports.sendClassReminders = functions.pubsub.schedule("every 5 minutes").onRun(async () => {
  const now = new Date();
  const upcomingTime = new Date(now.getTime() + 30 * 60 * 1000); // 30 minutes later
  const snapshot = await admin.firestore().collection("classes")
    .where("startTime", ">=", now.toISOString())
    .where("startTime", "<=", upcomingTime.toISOString())
    .get();
  const emails = snapshot.docs.map(doc => ({
    to: doc.data().userEmail,
    subject: `Reminder: Your class '${doc.data().className}' starts soon!`,
    text: `Your class starts at ${doc.data().startTime}. Be ready!`

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **firebase reminders configuration** | Core idea of this note | “I can explain firebase reminders configuration without jargon.” |
| **idempotent** | Safe to retry | “Retries must not double-charge.” |
| **config** | Knobs outside code | “Env-specific values stay out of source.” |

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
