[[java]] [[android]] [[golang]]

# Kotlin syntax (quick reference)

> JVM-null-safe language — `?.`, `!!`, `val`/`var`, and extension functions; use this note for day-one reading code, not full language spec.

## Mental model

Kotlin targets JVM/JS/Native. **`val`** immutable reference, **`var`** mutable. Nullability enforced at compile time: `String` vs `String?`.

```
Java null check     →  Kotlin ?.  ?:  !!
Java static         →  object / companion object
Java getter/setter  →  property syntax
```

## Standard config / commands

### Basics

```kotlin
val name: String = "app"      // read-only
var count = 0                 // inferred Int

fun greet(who: String = "world"): String = "Hello, $who"

if (x is String) println(x.length)  // smart cast after is
```

### Null safety

```kotlin
val len = text?.length              // Int? — null if text null
val safe = text?.length ?: 0        // Elvis — default 0
val forced = text!!.length          // NPE if text null — avoid in prod

// Safe call chain
user?.profile?.avatar?.url
```

### `!!` — when and why not

```kotlin
binding.progressBar!!.visibility = View.GONE
// Asserts non-null for platform/view code after findViewById
// Prefer: binding.progressBar?.visibility = View.GONE
// Or: requireNotNull(binding.progressBar) { "missing id" }
```

### Classes / data

```kotlin
data class User(val id: Long, val email: String)

class Repo(private val api: Api) {
    fun load() = api.fetch()
}
```

### Object & companion (static-like)

```kotlin
object Config {
    const val TIMEOUT = 30
}

class Factory {
    companion object {
        fun create(): Factory = Factory()
    }
}
```

### Extensions

```kotlin
fun String.isEmail(): Boolean = "@" in this
```

### Scope functions (pick by intent)

| Fn | `this`/`it` | Use |
|----|-------------|-----|
| `let` | `it` | null-safe block + result |
| `run` | `this` | configure object + result |
| `apply` | `this` | configure, return receiver |
| `also` | `it` | side effect, return receiver |

```kotlin
user?.let { u -> sendWelcome(u.email) }
```

### Collections

```kotlin
val xs = listOf(1, 2, 3)
val map = xs.associateWith { it * 2 }
xs.filter { it > 1 }.map { it.toString() }
```

### Coroutines (Android / backend)

```kotlin
suspend fun load(): Data = withContext(Dispatchers.IO) {
    api.fetch()
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NPE at `!!` | View/binding not inflated | Use view binding; `?.` or `requireNotNull` |
| Smart cast impossible | `var` mutated across threads | Copy to local `val` before check |
| Platform type warning | Java API returns unknown null | Annotate Java `@Nullable` / `@NonNull` or explicit Kotlin type |
| `when` not exhaustive | Sealed/interface not covered | Add branches or `else` |
| Coroutine crash | Blocking on Main | `withContext(IO)` for network/disk |

## Gotchas

> [!WARNING]
> **`!!` in UI code** — crashes users instead of failing gracefully; treat as code smell except generated binding guarantees.

> [!WARNING]
> **Java interop null** — Java `String` becomes platform type; assume nullable unless annotated.

> [!WARNING]
> **`==` is structural equality** — reference equality is `===`.

## When NOT to use

- **Full Kotlin course** — this is a cheat sheet; use official docs for coroutines flow, inline classes, DSL builders.
- **`!!` to silence compiler** — fix nullability model instead.

## Related

[[java]] [[android]] [[golang]] [[Design pattern]]
