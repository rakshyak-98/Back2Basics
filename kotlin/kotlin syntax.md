[[java]] [[android]] [[kotlin data flow]] [[kotlin view]]

# Kotlin syntax

> JVM/JS/Native language with null-safe types — `val`/`var`, smart casts, data classes, and concise functions that interop with Java.

```txt
        Kotlin syntax ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe null safety (`?.`, `?:`, `!!`), `val` vs `var`, data class…

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

## Mistakes to Avoid
- **Mistake:** Sprinkling `!!` to silence the compiler
- **Mistake:** Mutating `val` list contents and calling it “immutable” (referen…
- **Mistake:** Ignoring Java nullable annotations when crossing APIs

## Pros/Cons or Trade-offs
- **Pro:** Null safety and concision cut boilerplate.
- **Con:** `!!` and platform types from Java can reintroduce NPE footguns.

## Comparison
- vs Java: same ecosystem, stronger null model and less ceremony.
- vs [[dart]]: similar modern-null ideas; different runtimes (JVM vs Flutter/Dart VM).


### Use cases
- Android and backend JVM services: fewer NPEs, clearer models with `data class…

- **Example:** Replace `if (x != null) x.foo()` chains with `x?.foo()` and Elvi…
