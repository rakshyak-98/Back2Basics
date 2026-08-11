[[kotlin]]

# kotlin data flow

> kotlin data flow — by lets one object handle that logic of property on behalf of another object.

---

## Mental model

**Say it in one breath:** kotlin data flow — plain job, how I run it, how I know it’s broken.


`by` lets one object handle that logic of property on behalf of another object.
```kotlin
class User {
	val name: String
	get() {
		// custom logic
	}
}
```
- you can move that logic into a separate reusable class and delegate to it.
**Without delegation**
```kotlin
class User {
	private var _config: Config? = null_
	val config: Config
		get() {
			if (_config == null){
				_config = loadConfig()
			}
			return _config!!
		}
}
```
**With delegation**
```kotlin
val config by lazy {
	loadConfig();
}
```
Why was it added?
- To avoid repeating common property behavior.
- instead of implementing these in every class, Kotlin lets you resuse them through delegation.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **kotlin data flow** | Core idea of this note | “I can explain kotlin data flow without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[kotlin]]
