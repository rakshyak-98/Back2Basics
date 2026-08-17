[[symmetrical encryption]] [[HMAC (Hash based Message Authentication Codes)]] [[openssl]] [[Authentication terms]] [[Securing a hash key authentication]] [[JWT authentication]]

# yescrypt (yashcrypt)

> Memory-hard password hashing (yescrypt; filename typo for yescrypt) — raises attacker RAM cost per guess versus fast hashes.





## Interview Relevance
Password storage: memory-hard KDFs (yescrypt/scrypt/Argon2) raise attacker cost versus fast hashes like SHA-256.

## Sources
- [yescrypt — password hashing scheme](https://www.openwall.com/yescrypt/) — deep-dive
- [OWASP — Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) — overview

## Core Definition
yescrypt is a memory-hard password hashing KDF (scrypt successor); the vault filename `yashcrypt.md` is a typo for yescrypt.

## Key Concepts
**yescrypt** is a **password hashing** function (not general encryption), designed for **stored credentials**:

```txt
password + salt + params → yescrypt → fixed hash stored in DB
Login: recompute and constant-time compare
```

versus fast hashes (SHA256, MD5): offline attacker tries billions/sec.

versus **bcrypt/argon2/scrypt**: yescrypt adds **ROM-dependent** and **memory-hard** phases — parallel GPUs/ASICs need proportional RAM per guess.

Used where:
- Linux **libxcrypt** `$y$` hashes (glibc 2.36+)
- Distributions migrating from SHA512 crypt

**If you encounter unknown `yashcrypt` in legacy docs:** treat as **yescrypt** or verify against system `crypt(3)` man page — do not invent a custom algorithm.

## Technical Details
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

**Why application-layer KDF:** you control cost parameters per hardware generation; not tied to `/etc/shadow` format.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Login fail after distro upgrade | Hash method changed | Rehash on successful login (upgrade path) |
| Slow login under load | yescrypt memory cost high | Tune cost; offload to dedicated auth |
| Incompatible hash format | `$y$` vs `$6$` vs `$2b$` | Detect prefix; migrate gradually |
| Unknown `yashcrypt` reference | Typo / internal name | Map to yescrypt or audit codebase |

## Real-World Applications
Store password hashes with yescrypt (or Argon2id) parameters tuned for your login latency budget.

## Pros/Cons or Trade-offs
- **Pro:** Memory-hard hashing raises offline cracking cost dramatically.
- **Con:** Don't use password KDFs for **API signing** or **session tokens** — use [[HMAC (Hash based Message Authentication Codes)]] or random opaque tokens. KDFs are slow by design.

## Comparison
- vs fast hashes (SHA-256): password KDFs must be slow/memory-hard.
- vs [[HMAC (Hash based Message Authentication Codes)]]: HMAC authenticates messages; yescrypt hashes passwords for storage.

## Mistakes to Avoid
- Never SHA256(password) for storage — use yescrypt/argon2/bcrypt/scrypt.
- Per-user random salt — mandatory; prevents rainbow tables.
- Constant-time compare — timing leaks hash prefix.
- Filename typo `yashcrypt` — grep codebase for actual library import before assuming algorithm.
