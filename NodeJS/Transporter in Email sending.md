[[NodeJS]] [[SMTP]] [[mail server]] [[webhook]]

# Nodemailer Transporter

> Nodemailer Transporter — in Nodemailer, a Transporter is the long-lived object that knows *how* to deliver mail (host, port, credentials, TLS). You call transporter.sendMail(mailOptions) per message.

```txt
        Nodemailer Transpo ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Nodemailer Transporter** to see if you understand what i…

## Sources
- [Wikipedia — Transporter in Email sending](https://en.wikipedia.org/wiki/Transporter_in_Email_sending) — overview

## Key Concepts
- **In:** Nodemailer**:** In **Nodemailer**, a **Transporter** is the long-lived object…
- **Separate:** envelope**:** Separate **envelope** (SMTP `MAIL FROM`/`RCPT TO`) from **heade…


- **Core:** In **Nodemailer**, a **Transporter** is the long-lived object that knows *how…

## Technical Details
- In **Nodemailer**, a **Transporter** is the long-lived object that knows *how…
- You call `transporter.sendMail(mailOptions)` per message.

```
App boot → createTransport(config) → verify (optional)
                │
Each email ─────┴──► sendMail({ from, to, subject, html })
                         │
                         └── SMTP session (587 STARTTLS or 465 SMTPS)
```

- Separate **envelope** (SMTP `MAIL FROM`/`RCPT TO`) from **headers** (`From:` …
- Production apps pool one transporter; don't create per request.

### SMTP transporter (submission port 587)

```javascript
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: 587,
  secure: false,              // true for 465; false + STARTTLS for 587
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
  pool: true,                 // reuse connections
  maxConnections: 5,
  maxMessages: 100,
});

// Fail fast at deploy
await transporter.verify();
```

### Send mail

```javascript
const info = await transporter.sendMail({
  from: '"App" <noreply@example.com>',
  to: 'user@example.com',
  subject: 'Reset password',
  text: 'Plain fallback',
  html: '<p>HTML body</p>',
  replyTo: 'support@example.com',
});

console.log(info.messageId, info.response);
```

### Implicit TLS (port 465)

```javascript
nodemailer.createTransport({
  host: 'smtp.example.com',
  port: 465,
  secure: true,
});
```

### AWS SES / SendGrid

```javascript
// SES: use aws-sdk transport or SMTP credentials from SES console
// SendGrid: host smtp.sendgrid.net, user apikey, pass SG.xxx
```

### Debug SMTP dialog

```javascript
createTransport({ ..., logger: true, debug: true });
```

## Mistakes to Avoid
- **Mistake:** **`rejectUnauthorized: false`**
- **Mistake:** **New transporter per request**
- **Mistake:** **Display From ≠ authenticated domain**
- **Mistake:** **Sync send in request path**
- **Mistake:** **`ECONNECTION` / timeout:** check Firewall, wrong port
- **Mistake:** **Auth failed:** check Credentials, IP allowlist
- **Mistake:** **Mail in spam:** check SPF/DKIM/DMARC
- **Mistake:** **`self signed certificate`:** check Corporate MITM TLS
- **Mistake:** **Intermittent slow sends:** check No pooling
- **Mistake:** **Message accepted but not delivered:** check Provider dashboard

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Nodemailer Transporter — in Nodemailer, a Transporter is the long-lived object t…).
- **Con / when not:** **High volume marketing mail**
- **Con / when not:** **Receiving mail**

## Comparison
- vs [[SMTP]]: know when each applies


### Use cases
- In production APIs and tooling, **Transporter in Email sending** shows up whe…
