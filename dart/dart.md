[[dart functions]] [[flutter]] [[kotlin syntax]]

# Dart

> Language behind Flutter (and more) — sound null safety, isolates instead of shared-memory threads, and factories that can return subtypes or cached instances.





## Interview Relevance
Interviewers contrast Dart null safety with Java, explain isolates vs threads, and ask when a `factory` constructor beats a generative one.

## Sources
- [Dart language tour](https://dart.dev/language) — deep-dive
- [Dart — Null safety](https://dart.dev/null-safety) — overview

## Key Concepts
- **Null safety:** `String` vs `String?` at compile time.
- **Isolates:** memory-isolated concurrency; message passing.
- **Constructors:** generative vs `factory` (can return existing instance/subtype).
- **async/await:** Futures and Streams for I/O.

## Technical Details
```dart
factory User.fromJson(Map<String, dynamic> json) {
  return User(json['name'] as String);
}
```

A `factory` constructor can return a subtype or cached object — unlike a normal generative constructor that always creates a new instance of exactly that class.

| Feature | Role |
|---------|------|
| `var`/`final`/`const` | Mutability / compile-time const |
| `async` | Future-based concurrency |
| Isolates | Parallelism without shared mutable heap |

## Real-World Applications
Flutter apps: UI in Dart, heavy parse work in an isolate, factories for JSON models.

**Example:** `factory` on an immutable model returns a canonical instance from a pool for identical keys.

## Pros/Cons or Trade-offs
- **Pro:** Strong null safety and Flutter productivity.
- **Con:** Isolate model requires explicit message passing for CPU parallelism.

## Comparison
- vs [[kotlin syntax]]: both modern null-safe; Dart pairs tightly with Flutter.
- vs JS: Dart is typed/AOT-friendly for mobile release builds.

## Mistakes to Avoid
- Using `!` bang operators everywhere to silence null safety.
- Assuming isolates share global mutable memory like threads.
- Blocking the UI isolate with heavy sync work.
