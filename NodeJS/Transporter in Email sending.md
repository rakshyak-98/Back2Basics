[[NodeJS]] [[SMTP]] [[E mail server]]

# Nodemailer Transporter

> One-line: configured SMTP (or SES/transport plugin) instance that sends mail — create once at boot, reuse for all messages; auth and TLS live on the transporter.

## Mental model

In **Nodemailer**, a **Transporter** is the long-lived object that knows *how* to deliver mail (host, port, credentials, TLS). You call `transporter.sendMail(mailOptions)` per message.

```
App boot → createTransport(config) → verify (optional)
                │
Each email ─────┴──► sendMail({ from, to, subject, html })
                         │
                         └── SMTP session (587 STARTTLS or 465 SMTPS)
```

Separate **envelope** (SMTP `MAIL FROM`/`RCPT TO`) from **headers** (`From:` display vs bounce address). Production apps pool one transporter; don't create per request.

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ECONNECTION` / timeout | Firewall, wrong port | 587 vs 465; `secure` flag; security group |
| Auth failed | Credentials, IP allowlist | Rotate app password; enable SMTP auth on provider |
| Mail in spam | SPF/DKIM/DMARC | DNS records; align `From` domain with SMTP auth domain |
| `self signed certificate` | Corporate MITM TLS | Provide `tls.ca` or fix proxy; never `rejectUnauthorized: false` in prod |
| Intermittent slow sends | No pooling | `pool: true`; reuse transporter singleton |
| Message accepted but not delivered | Provider dashboard | Check bounce/webhook; verify `MAIL FROM` domain |

## Gotchas

> [!WARNING]
> **`rejectUnauthorized: false`** — disables TLS verification; use only in dev with known MITM.

> [!WARNING]
> **New transporter per request** — TCP+TLS handshake every email; rate limits and latency spike.

> [!WARNING]
> **Display From ≠ authenticated domain** — Gmail/Outlook reject or spam-folder misaligned From.

> [!WARNING]
> **Sync send in request path** — queue outbound mail (Bull, SQS) for user-facing latency.

## When NOT to use

- **High volume marketing mail** — dedicated ESP API (SendGrid/Mailgun) with webhooks, not raw SMTP from app servers.
- **Receiving mail** — transporter is outbound only; use [[IMAP (Internet Message Access Protocol)]] / [[POP3 (Post Office Protocol v3)]] for inbound.

## Related

[[SMTP]] [[E mail server]] [[NodeJS]] [[webhook]]
