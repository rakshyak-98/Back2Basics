[[java]] [[android]] [[kotlin data flow]] [[kotlin view]]

# Kotlin syntax

> JVM/JS/Native language with null-safe types — `val`/`var`, smart casts, data classes, and concise functions that interop with Java.

## Interview Relevance

Interviewers probe null safety (`?.`, `?:`, `!!`), `val` vs `var`, data classes, coroutines at a high level, and Java interop gotchas.

## Sources

- [Kotlin — Basic syntax](https://kotlinlang.org/docs/basic-syntax.html) — overview
- [Kotlin — Null safety](https://kotlinlang.org/docs/null-safety.html) — deep-dive

## Key Concepts

- **`val` / `var`:** read-only reference vs reassignable.
- **Null system:** `String` vs `String?` enforced at compile time.
- **Smart cast:** after `is` checks, the compiler narrows types.
- **`object` / `companion object`:** singletons and Java-static-like APIs.
- **Properties:** replace Java getter/setter boilerplate.

## Technical Details

```kotlin
val name: String = "app"
var count = 0
fun greet(who: String = "world"): String = "Hello, $who"

val len = text?.length
val safe = text?.length ?: 0
// text!!.length  — avoid in production paths

if (x is String) println(x.length) // smart cast
```

| Java habit | Kotlin |
|------------|--------|
| null checks | `?.` `?:` |
| static | `object` / `companion` |
| getters/setters | properties |
| POJO | `data class` |

## Real-World Applications

Android and backend JVM services: fewer NPEs, clearer models with `data class`, gradual Java migration.

**Example:** Replace `if (x != null) x.foo()` chains with `x?.foo()` and Elvis defaults.

## Pros/Cons or Trade-offs

- **Pro:** Null safety and concision cut boilerplate.
- **Con:** `!!` and platform types from Java can reintroduce NPE footguns.

## Comparison

- vs Java: same ecosystem, stronger null model and less ceremony.
- vs [[dart]]: similar modern-null ideas; different runtimes (JVM vs Flutter/Dart VM).

## Mistakes to Avoid

- Sprinkling `!!` to silence the compiler.
- Mutating `val` list contents and calling it “immutable” (reference vs deep immutability).
- Ignoring Java nullable annotations when crossing APIs.
