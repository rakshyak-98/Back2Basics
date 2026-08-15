[[NodeJS]] [[npm command]] [[expressjs]] [[Packages/Ajv (Another JSON validator)]] [[Packages/node-cron]] [[Transporter in Email sending]]

# npm packages

> Field shortlist of common Node libs — what each is for and the footguns that show up in prod.

## Interview Relevance

Interviewers use **npm packages** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **extraneous**, **helmet / hpp**, **multer**.

## Sources

- [npm — Packages and modules](https://docs.npmjs.com/about-packages-and-modules) — overview
- [Wikipedia — npm packages](https://en.wikipedia.org/wiki/npm_packages) — overview

## Key Concepts

- **extraneous:** In node_modules, not in package.json — CI should fail or prune these.
- **helmet / hpp:** Security middleware — Headers + parameter pollution.
- **multer:** multipart uploads — Field name must match client FormData.

## Technical Details

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

## Real-World Applications

In production APIs and tooling, **npm packages** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Don’t set `Content-Type` on FormData fetch** — boundary breaks; browser sets it; **node-cron in many replicas** — jobs fire N times; see [[Packages/node-cron]].

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Field shortlist of common Node libs — what each is for and the footguns that sho…).
- **Con / when not:** **Replacing platform features** — prefer CDN/WAF rate limits when you have them.
- **Con / when not:** **Unmaintained utils** — check last publish before adding lodash-sized deps for one helper.

## Comparison

vs [[npm command]]: know when each applies — do not treat them as interchangeable. vs [[expressjs]]: know when each applies — do not treat them as interchangeable. vs [[Packages/Ajv (Another JSON validator)]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Don’t set `Content-Type` on FormData fetch** — boundary breaks; browser sets it.
- **node-cron in many replicas** — jobs fire N times; see [[Packages/node-cron]].
- **CORS fail:** check Origin + credentials; fix: Exact origin list; no `*` with cookies
- **multer empty:** check Field name / Content-Type; fix: Match names; don’t set CT manually with FormData
- **extraneous noise:** check `npm ls`; fix: Add dep or remove install
- **Rate limit false positives:** check Shared IP behind LB; fix: Trust proxy; key by user
