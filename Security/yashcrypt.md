[[symmetrical encryption]] [[HMAC (Hash based Message Authentication Codes)]] [[openssl]]

# yescrypt (yashcrypt)

> Memory-hard password hashing KDF — successor to scrypt; increases attacker cost by requiring large RAM per guess. Filename `yashcrypt.md` is a vault typo for **yescrypt**.

---

## Mental model

**yescrypt** is a **password hashing** function (not general encryption), designed for **stored credentials**:

```txt
password + salt + params → yescrypt → fixed hash stored in DB
Login: recompute and constant-time compare
```

vs fast hashes (SHA256, MD5): offline attacker tries billions/sec.

vs **bcrypt/argon2/scrypt**: yescrypt adds **ROM-dependent** and **memory-hard** phases — parallel GPUs/ASICs need proportional RAM per guess.

Used where:
- Linux **libxcrypt** `$y$` hashes (glibc 2.36+)
- Distributions migrating from SHA512 crypt

**If you encounter unknown `yashcrypt` in legacy docs:** treat as **yescrypt** or verify against system `crypt(3)` man page — do not invent a custom algorithm.

---

## Standard config / commands

### Linux password hash (yescrypt)

```bash
# /etc/login.defs
ENCRYPT_METHOD YESCRYPT

# Generate hash (example — use passwd/usermod in practice)
python3 -c "import crypt; print(crypt.crypt('testpass', crypt.mksalt(crypt.METHOD_YESCRYPT)))"
```

### Prefer argon2/bcrypt in application DBs

```python
# argon2-cffi (recommended for app-layer passwords)
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=4)
hash = ph.hash("user-password")
ph.verify(hash, "user-password")
```

```javascript
// bcrypt (widely supported)
import bcrypt from 'bcrypt';
const hash = await bcrypt.hash(password, 12);
await bcrypt.compare(password, hash);
```

**Why app-layer KDF:** you control cost params per hardware generation; not tied to `/etc/shadow` format.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Login fail after distro upgrade | Hash method changed | Rehash on successful login (upgrade path) |
| Slow login under load | yescrypt memory cost high | Tune cost; offload to dedicated auth |
| Incompatible hash format | `$y$` vs `$6$` vs `$2b$` | Detect prefix; migrate gradually |
| Unknown `yashcrypt` reference | Typo / internal name | Map to yescrypt or audit codebase |

---

## Gotchas

> [!WARNING]
> **Never SHA256(password) for storage** — use yescrypt/argon2/bcrypt/scrypt.

> [!WARNING]
> **Per-user random salt** — mandatory; prevents rainbow tables.

> [!WARNING]
> **Constant-time compare** — timing leaks hash prefix.

> [!WARNING]
> **Filename typo `yashcrypt`** — grep codebase for actual library import before assuming algorithm.

---

## When NOT to use

Don't use password KDFs for **API signing** or **session tokens** — use [[HMAC (Hash based Message Authentication Codes)]] or random opaque tokens. KDFs are slow by design.

---

## Related

[[HMAC (Hash based Message Authentication Codes)]] [[Authentication terms]] [[Securing a hash key authentication]] [[JWT authentication]]
