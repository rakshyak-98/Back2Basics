[[kotlin syntax]] [[kotlin view]] [[Design pattern/Proxy]]

# Kotlin property delegation

> `by` hands a property’s getter/setter logic to another object — reuse lazy load, observables, and map-backed fields without boilerplate.





## Interview Relevance
Interviewers want `by lazy`, custom `ReadOnlyProperty`, and how delegation differs from inheritance for cross-cutting property behavior.

## Sources
- [Kotlin — Delegated properties](https://kotlinlang.org/docs/delegated-properties.html) — deep-dive
- [Kotlin — Lazy](https://kotlinlang.org/docs/delegated-properties.html#lazy-properties) — overview

## Key Concepts
- **`by`:** property delegates to an object implementing the property protocol.
- **`lazy`:** thread-safe (configurable) one-time initialization.
- **`observable` / `vetoable`:** hooks on change.
- **Map delegation:** properties backed by a `Map` for dynamic payloads.

## Technical Details
Without delegation (manual lazy):

```kotlin
class User {
  private var _config: Config? = null
  val config: Config
    get() {
      if (_config == null) _config = loadConfig()
      return _config!!
    }
}
```

With delegation:

```kotlin
class User {
  val config: Config by lazy { loadConfig() }
}
```

Custom getters can move into a reusable delegate class and be attached with `by`.

## Real-World Applications
Android ViewModels use `lazy` for expensive repositories; feature flags bind from maps via delegates.

**Example:** Repeated `loadConfig()` guards across classes → one `by lazy` pattern.

## Pros/Cons or Trade-offs
- **Pro:** Removes repetitive property plumbing; standard library delegates are well-known.
- **Con:** Magical `by` can hide cost (lazy locks, reflection-ish map delegates) if overused.

## Comparison
- vs inheritance: delegation composes behavior for a property, not the whole type.
- vs Java manual getters: same idea with less boilerplate.

## Mistakes to Avoid
- Using `lazy` for something that must refresh on every access.
- Assuming `lazy` is always unsynchronized — check the mode.
- Nesting heavy work in delegates without measuring startup jank.
