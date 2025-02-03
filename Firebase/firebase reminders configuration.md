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
  }));

  emails.forEach(async (email) => {
    await transporter.sendMail(email);
  });

  return null;
});

```

### Execution flow of Firebase Firestore reminder code
- the code will be triggered by a Cloud Scheduler (or a Firebase Cloud Function with a CRON job)