[[Design pattern/Singleton]] [[LLD/Questions/Logger]] [[zed config]]

# File-based configuration manager (LLD)

> Central loader for system settings from files — typed access, refresh rules, and safe defaults when files are missing or malformed.

```txt
        File-based configu ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** LLD reviews probe singleton vs injectability, hot reload vs restart, valid…

## Sources
- [12-Factor — Config](https://12factor.net/config/) — overview
- [Wikipedia — Configuration file](https://en.wikipedia.org/wiki/Configuration_file) — overview

## Key Concepts
- **Single source of truth API:** `get(key)` / typed getters.
- **Precedence:** explicit layering beats “last file wins” surprises.
- **Validation on load:** fail fast on required missing keys.
- **Reload policy:** watch file vs SIGHUP vs process restart.
- **Thread safety:** readers during reload need atomic swap of the immutable snapshot.

## Technical Details
```txt
defaults → config.yaml → ENV overrides → validate → immutable snapshot
```

| Concern | Approach |
|---------|----------|
| Bad YAML | Keep last good config; alarm |
| Secrets | Env/secret manager, not plaintext repo files |
| Multi-process | Each process loads; or push via side car |

## Mistakes to Avoid
- **Mistake:** Mutable global config mutated in place by callers
- **Mistake:** No schema validation
- **Mistake:** Storing passwords in the same committed file as harmless flags

## Pros/Cons or Trade-offs
- **Pro:** Simple ops story; easy to diff in git (non-secret parts).
- **Con:** File watchers and partial writes can tear if not handled.

## Comparison
- vs env-only 12-factor: files help nested structure; env still wins for secrets/prod variance.
- vs remote config services: files are simpler; remote adds central control and risk.


### Use cases
- Services read `/etc/myapp/config.yaml` at boot

- **Example:** Hot reload flips a feature flag without deploy
