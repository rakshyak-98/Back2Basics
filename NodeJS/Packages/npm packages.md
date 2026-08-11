[[NodeJS]] [[npm command]] [[expressjs]] [[Packages/Ajv (Another JSON validator)]] [[Packages/node-cron]]

# npm packages

> Field shortlist of common Node libs — what each is for and the footguns that show up in prod.

---

## Mental model

**Say it in one breath:** Prefer small, maintained packages with clear jobs — validation, security headers, uploads, HTTP clients — and declare them in `package.json` (extraneous = installed but undeclared).

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **extraneous** | In node_modules, not in package.json | “CI should fail or prune these.” |
| **helmet / hpp** | Security middleware | “Headers + parameter pollution.” |
| **multer** | multipart uploads | “Field name must match client FormData.” |

## Standard config / commands

| Package | Job |
|---------|-----|
| **helmet** | Secure HTTP headers |
| **cors** | Browser cross-origin policy |
| **express-rate-limit** | Basic abuse throttle |
| **compression** | gzip responses |
| **multer** | multipart file upload |
| **nodemailer** | SMTP send |
| **got** / undici | HTTP client |
| **yup** / [[Packages/Ajv (Another JSON validator)\|Ajv]] | Input validation |
| **ms** | Parse durations to ms |
| **file-type** | Sniff binary types |
| **hpp** | HTTP parameter pollution |
| **[[Packages/node-cron\|node-cron]]** | In-process schedules |

```js
origin: (origin, cb) => {
  const allowed = ['https://mydomain.com']
  if (!origin || allowed.includes(origin)) return cb(null, true)
  cb(new Error('Not allowed by CORS'))
}
```

| multer API | Client FormData |
|------------|-----------------|
| `single('file')` | `append('file', file)` |
| `array('files', 5)` | multiple `append('files', …)` |
| `fields([{ name: 'avatar' }])` | matching keys |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| CORS fail | Origin + credentials | Exact origin list; no `*` with cookies |
| multer empty | Field name / Content-Type | Match names; don’t set CT manually with FormData |
| extraneous noise | `npm ls` | Add dep or remove install |
| Rate limit false positives | Shared IP behind LB | Trust proxy; key by user |

---

## Gotchas

> [!WARNING]
> **Don’t set `Content-Type` on FormData fetch** — boundary breaks; browser sets it.

> [!WARNING]
> **node-cron in many replicas** — jobs fire N times; see [[Packages/node-cron]].

---

## When NOT to use

- **Replacing platform features** — prefer CDN/WAF rate limits when you have them.
- **Unmaintained utils** — check last publish before adding lodash-sized deps for one helper.

---

## Related

[[npm command]] [[expressjs]] [[Packages/Ajv (Another JSON validator)]] [[Packages/node-cron]] [[Transporter in Email sending]]
