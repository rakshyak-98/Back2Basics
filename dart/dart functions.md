[[flutter]] [[Descriptive/JavaScript/function]]

# Dart functions

> First-class, closable functions with optional/named params, cascade-friendly syntax, and nested functions for encapsulation — know closure capture and `=>` vs block bodies.

## Mental model

Functions are objects: assign to variables, pass as args, return from functions. Dart is single-threaded event-loop async ([[flutter]] isolates for parallelism).

```
Top-level fn
    │
    ├── nested fn (closes over outer locals)
    ├── tear-off: obj.method  → bound closure
    └── typedef / Function type for callbacks
```

Parameter forms: positional, optional positional `[ ]`, named `{ }`, required named `{required x}`.

## Standard config / commands

### Declarations

```dart
// Full form
int sum(int a, int b) {
  return a + b;
}

// Arrow (expression body)
int sum(int a, int b) => a + b;

// Optional positional
void log(String msg, [int level = 0]) {}

// Named (call sites use names — API clarity)
void connect({required String host, int port = 5432}) {}

connect(host: 'db.internal', port: 5432);
```

### First-class and typedef

```dart
typedef Compare<T> = int Function(T a, T b);

int sortKey(String a, String b) => a.compareTo(b);
final Compare<String> cmp = sortKey;
list.sort(cmp);
```

### Nested functions (constructor / method scope)

```dart
class Parser {
  Parser() {
    int depth = 0;

    void enter() => depth++;
    void leave() {
      if (depth > 0) depth--;
    }

    // use enter/leave only inside constructor logic
  }
}
```

### Closures

```dart
Function makeAdder(int add) {
  return (int x) => x + add; // captures add
}
```

### Generics

```dart
T identity<T>(T value) => value;
```

### Async functions

```dart
Future<User> fetchUser(String id) async {
  final res = await http.get(Uri.parse('/users/$id'));
  return User.fromJson(jsonDecode(res.body));
}
```

### Tear-offs

```dart
final fn = myObj.handle; // bound if instance method
list.forEach(print);     // top-level tear-off
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Required named parameter missing" | Call without `required` arg | Pass named param or give default |
| Closure sees stale value | Captured loop variable (pre-Dart 3) | Use `for (final x in xs)` or copy local |
| `void` callback return ignored | Returning value from `void` fn | Change return type or don't return |
| Stack overflow | Unbounded recursion | Iterate or tail-call refactor |
| Type error on Function | Raw `Function` vs typed | Use `void Function(int)` or typedef |
| Nested fn not visible outside | Scope is lexical | Move to private top-level `_helper` if needed wider |

## Gotchas

> [!WARNING]
> **Named params are not optional by default** — mark `{required foo}` or provide default; unlike JS object destructuring defaults alone.

> [!WARNING]
> **`async` returns Future immediately** — errors become async errors; use `try/catch` inside async fn.

> [!WARNING]
> **Nested functions in hot paths** — recreated each call if inside method body; hoist to private method or top-level for clarity/perf.

> [!WARNING]
> **Equality on Function** — closures are never equal unless same reference; don't use as Map keys without care.

## When NOT to use

- **Nested functions for large logic** — extract class or top-level private function for testability.
- **Dynamic `Function` everywhere** — defeats analyzer; use typedefs/generics.
- **Isolates for tiny work** — message copy cost; use compute/isolate only for CPU-heavy jobs.

## Related

[[flutter]] [[Descriptive/JavaScript/function]] [[Callback]]
