[[dart functions]] [[flutter/flutter widget]]

# dart

> Dart is Flutter's language — strong typing, async/await, and factory constructors for flexible object creation from JSON and caches.

## Mental model

**Say it in one breath:** A `factory` constructor can return an existing instance or a subclass, which is ideal for parsing JSON into fully populated model objects.

```dart
factory ApiRoomData.fromJson(Map<String, dynamic> json) {
  return ApiRoomData(
    // map fields from json
  );
}
```

| Concept | Meaning |
| --- | --- |
| `Map<String, dynamic>` | JSON object shape — string keys, values of any type |
| `factory` | Unlike a normal constructor, may return a cached or subtype instance |
| `fromJson` | Common pattern for API deserialization |

## Standard config / commands

```bash
dart --version
dart run bin/main.dart
flutter pub get
dart analyze
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `type 'Null' is not a subtype` | Missing JSON field | Nullable types (`String?`) or defaults in `fromJson` |
| Factory returns wrong type | Constructor body | Ensure factory returns correct class |
| Analyzer errors on `dynamic` | Implicit casts | Add explicit types or use `json_serializable` |

## Gotchas

> [!WARNING]
> **`dynamic` hides bugs until runtime** — prefer generated serializers for production models.

## When NOT to use

- **Heavy logic in `fromJson`** — move validation to a dedicated mapper or use `freezed` / `json_serializable`.

## Related

[[dart functions]] [[flutter/flutter widget]] [[flutter/flutter build]]
