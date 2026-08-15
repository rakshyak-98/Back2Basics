[[NodeJS]] [[SMTP]] [[E mail server]] [[webhook]]

# Nodemailer Transporter

> Nodemailer Transporter — in Nodemailer, a Transporter is the long-lived object that knows *how* to deliver mail (host, port, credentials, TLS). You call transporter.sendMail(mailOptions) per message.

## Interview Relevance

Interviewers probe **Nodemailer Transporter** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Wikipedia — Transporter in Email sending](https://en.wikipedia.org/wiki/Transporter_in_Email_sending) — overview

## Core Definition

In **Nodemailer**, a **Transporter** is the long-lived object that knows *how* to deliver mail (host, port, credentials, TLS). You call `transporter.sendMail(mailOptions)` per message.

## Key Concepts

- In **Nodemailer**, a **Transporter** is the long-lived object that knows *how* to deliver mail (host, port, credentials, TLS). You call `transporter.sendMail(mailOptions)` per m…
- Separate **envelope** (SMTP `MAIL FROM`/`RCPT TO`) from **headers** (`From:` display versus bounce address). Production apps pool one transporter; don't create per request.

## Technical Details

In **Nodemailer**, a **Transporter** is the long-lived object that knows *how* to deliver mail (host, port, credentials, TLS). You call `transporter.sendMail(mailOptions)` per message.

```
App boot → createTransport(config) → verify (optional)
                │
Each email ─────┴──► sendMail({ from, to, subject, html })
                         │
                         └── SMTP session (587 STARTTLS or 465 SMTPS)
```

Separate **envelope** (SMTP `MAIL FROM`/`RCPT TO`) from **headers** (`From:` display versus bounce address). Production apps pool one transporter; don't create per request.

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

## Real-World Applications

In production APIs and tooling, **Transporter in Email sending** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`rejectUnauthorized: false`** — disables TLS verification; use only in dev with known MITM; **New transporter per request** — TCP+TLS handshake every email; rate limits and latency spike.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Nodemailer Transporter — in Nodemailer, a Transporter is the long-lived object t…).
- **Con / when not:** **High volume marketing mail** — dedicated ESP API (SendGrid/Mailgun) with webhooks, not raw SMTP from application servers.
- **Con / when not:** **Receiving mail** — transporter is outbound only; use [[IMAP (Internet Message Access Protocol)]] / [[POP3 (Post Office Protocol v3)]] for inbound.

## Comparison

vs [[SMTP]]: know when each applies — do not treat them as interchangeable. vs [[E mail server]]: know when each applies — do not treat them as interchangeable. vs [[webhook]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`rejectUnauthorized: false`** — disables TLS verification; use only in dev with known MITM.
- **New transporter per request** — TCP+TLS handshake every email; rate limits and latency spike.
- **Display From ≠ authenticated domain** — Gmail/Outlook reject or spam-folder misaligned From.
- **Sync send in request path** — queue outbound mail (Bull, SQS) for user-facing latency.
- **`ECONNECTION` / timeout:** check Firewall, wrong port; fix: 587 vs 465; `secure` flag; security group
- **Auth failed:** check Credentials, IP allowlist; fix: Rotate app password; enable SMTP auth on provider
- **Mail in spam:** check SPF/DKIM/DMARC; fix: DNS records; align `From` domain with SMTP auth domain
- **`self signed certificate`:** check Corporate MITM TLS; fix: Provide `tls.ca` or fix proxy; never `rejectUnauthorized: false` in prod
- **Intermittent slow sends:** check No pooling; fix: `pool: true`; reuse transporter singleton
- **Message accepted but not delivered:** check Provider dashboard; fix: Check bounce/webhook; verify `MAIL FROM` domain
