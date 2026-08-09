[[Security]]

# Base64

> Base64 — turn binary data (like images, files, PDFs) into plain text so it can be safely sent over the internet or stored in places that only allow

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Base64 — I can explain the job, the config, and the top failure without jargon.


turn binary data (like images, files, PDFs) into plain text so it can be safely sent over the internet or stored in places that only allow text.
> [!INFO]
> You cannot paste raw photo bytes (binary data) into an email or JSON. So Base64 converts that photo into a long string of letters, numbers, and symbols
> Base64 strings are ~33% larger than the original file.
**Image in HTML**
```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ..." />
```
### How It Works (Simple Math)
- Normal text uses **8 bits per character** (1 byte)
- Base64 uses **64 safe characters**: A–Z, a–z, 0–9, +, / (and = for padding)
It takes **3 bytes** of binary data (24 bits) → splits into **4 characters** (6 bits each)

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Base64** | This note’s core idea | “I explain Base64 in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

---

## Standard config / commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Apply/deploy fail | plan / events | Fix IAM or syntax |
| TLS/DNS wrong | dig / openssl | Fix records and certs |
| Secret leak risk | repo scan | Rotate; use secret store |

---

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---

## When NOT to use

- Skip when a simpler existing approach already fits.

---

## Related

[[Security]]
