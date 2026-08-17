[[Security]]

# Base64

> Turn binary into ASCII text for protocols and configs that dislike raw bytes — encoding, not encryption.

```txt
        Base64 ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Why It Matters
- **Key signal:** Quick filter: Base64 is encoding, not encryption

## Sources
- [RFC 4648 — The Base16, Base32, and Base64 Data Encodings](https://www.rfc-editor.org/rfc/rfc4648) — deep-dive
- [Wikipedia — Base64](https://en.wikipedia.org/wiki/Base64) — overview

## Key Concepts
- **Note:** turn binary data (like images, files, PDFs) into plain text so it can be safe…
> [!INFO]
> You cannot paste raw photo bytes (binary data) into an email or JSON. So Base64 converts that photo into a long string of letters, numbers, and symbols
> Base64 strings are ~33% larger than the original file.
**Image in HTML**
```html
- **Note:** <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ.…
```
### How It Works (Simple Math)
- **Normal text:** Normal text uses **8 bits per character** (1 byte)
- **Base64 uses:** Base64 uses **64 safe characters**: A–Z, a–z, 0–9, +, / (and = for padding)
- **Note:** It takes **3 bytes** of binary data (24 bits) → splits into **4 characters** …

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Base64** | This note’s core idea | “I explain Base64 in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |


- **Core:** Base64 encodes binary as ASCII text using a 64-character alphabet so binary c…

## Technical Details
```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Apply/deploy fail | plan / events | Fix IAM or syntax |
| TLS/DNS wrong | dig / openssl | Fix records and certs |
| Secret leak risk | repo scan | Rotate; use secret store |

## Mistakes to Avoid
- **Mistake:** Prefer words you can say aloud in a review

## Pros/Cons or Trade-offs
- **Pro:** Safe binary-in-text transport for PEMs, JWTs, and protocols.
- **Con:** Skip when a simpler existing approach already fits.

## Real-World Applications
- **Scenario:** PEM certificates, JWT parts, and `data:` URLs all carry binary as Base64 text
