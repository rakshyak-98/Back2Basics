[[dart functions]] [[flutter]] [[kotlin syntax]]

# Dart

> Language behind Flutter (and more) — sound null safety, isolates instead of shared-memory threads, and factories that can return subtypes or cached instances.

```txt
        Dart ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers contrast Dart null safety with Java, explain isolates vs threads…

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

- A `factory` constructor can return a subtype or cached object

| Feature | Role |
|---------|------|
| `var`/`final`/`const` | Mutability / compile-time const |
| `async` | Future-based concurrency |
| Isolates | Parallelism without shared mutable heap |

## Mistakes to Avoid
- **Mistake:** Using `!` bang operators everywhere to silence null safety
- **Mistake:** Assuming isolates share global mutable memory like threads
- **Mistake:** Blocking the UI isolate with heavy sync work

## Pros/Cons or Trade-offs
- **Pro:** Strong null safety and Flutter productivity.
- **Con:** Isolate model requires explicit message passing for CPU parallelism.

## Comparison
- vs [[kotlin syntax]]: both modern null-safe; Dart pairs tightly with Flutter.
- vs JS: Dart is typed/AOT-friendly for mobile release builds.


### Use cases
- Flutter apps: UI in Dart, heavy parse work in an isolate, factories for JSON …

- **Example:** `factory` on an immutable model returns a canonical instance fro…
