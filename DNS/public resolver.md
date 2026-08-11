[[DNS]]

# public resolver

> public resolver — s (like 8.8.8.8 or 1.1.1.1) don’t store domain → IP mappings permanently.

---

## Mental model

**Say it in one breath:** public resolver — I can explain the job, the config, and the top failure without jargon.


### **1. Public resolver’s job**
Public resolvers (like `8.8.8.8` or `1.1.1.1`) **don’t store domain → IP mappings permanently**.
They act as **recursive resolvers**, meaning:
- They fetch the correct IP from the authoritative source on your behalf.
- They **cache** the answer temporarily (based on TTL).
### **2. Step-by-step resolution flow**
When you query `dig @8.8.8.8 example.com`, Google DNS performs this chain:
1. **Check local cache**
    - If already cached and TTL not expired → return instantly.
2. **If not cached → recursive lookup begins:**
    a. Ask **root DNS servers** → “who handles `.com` TLD?”
    b. `.com` TLD servers respond with NS (nameserver) for `example.com` (e.g. `ns1.examplehost.com`).
    c. Public resolver then asks that **authoritative nameserver** for `example.com` → “what is its A record?”
    d. Authoritative server replies: `example.com → 93.184.216.34`.
3. **Public resolver caches this** for the TTL (say, 3600s).
4. **Public resolver sends result back** to your machine.
### **3. Next requests**
When anyone else asks the same resolver for `example.com` within that TTL window,
it returns the **cached IP**, avoiding the full lookup chain.
### **4. Sum

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **public resolver** | This note’s core idea | “I explain public resolver in plain words.” |
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

[[DNS]]
