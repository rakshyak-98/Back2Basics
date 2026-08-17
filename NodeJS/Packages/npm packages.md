[[NodeJS]] [[npm command]] [[expressjs]] [[Packages/Ajv (Another JSON validator)]] [[Packages/node-cron]] [[Transporter in Email sending]]

# npm packages

> Field shortlist of common Node libs — what each is for and the footguns that show up in prod.

```txt
        npm packages ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **npm packages** to check whether you can explain the mechan…

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

## Mistakes to Avoid
- **Mistake:** **Don’t set `Content-Type` on FormData fetch**
- **Mistake:** **node-cron in many replicas**
- **Mistake:** **CORS fail:** check Origin + credentials
- **Mistake:** **multer empty:** check Field name / Content-Type
- **Mistake:** **extraneous noise:** check `npm ls`
- **Mistake:** **Rate limit false positives:** check Shared IP behind LB

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Field shortlist of common Node libs — what each is for and the footguns that sho…).
- **Con / when not:** **Replacing platform features**
- **Con / when not:** **Unmaintained utils**

## Comparison
- vs [[npm command]]: know when each applies


### Use cases
- In production APIs and tooling, **npm packages** shows up whenever teams ship…
