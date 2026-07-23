[[java]] [[kotlin]] [[Design pattern]] [[method shadowing]]

# Static members (class-level state and methods)

> Belong to the type, not instances — one shared slot in memory; no virtual dispatch; common for factories, constants, and caches; abuse causes test pain and hidden global state.

## Mental model

```
Class Loader loads MyClass
        │
        ▼
 Method area / metaclass ──► static fields initialized once
        │
        ▼
All instances share same static field memory
```

Static methods resolve at **compile time** by reference type — cannot override instance methods polymorphically ([[method shadowing]] hiding rules in Java).

Lifecycle: initialized when class first used (classloader `<clinit>`); order depends on dependency graph — fragile if circular.

## Standard config / commands

### Java

```java
public final class Config {
    private Config() {} // block instantiate

    public static final int MAX_RETRIES = 3;
    private static volatile DataSource ds;

    public static DataSource getDataSource() {
        if (ds == null) {
            synchronized (Config.class) {
                if (ds == null) ds = buildPool();
            }
        }
        return ds;
    }
}
```

### Kotlin — `companion object`

```kotlin
class Api {
    companion object {
        const val BASE_URL = "https://api.example.com"
        fun create(): Api = Api()
    }
}
// Api.BASE_URL, Api.create()
```

### C#-style pattern in Java — static factory

```java
public static User fromJson(String json) { ... }
```

### When static is appropriate

| Use | Example |
|-----|---------|
| Constants | `HTTP_OK = 200` |
| Pure utilities | `Math.max`, `Objects.requireNonNull` |
| Factory on type | `MyType.parse(String)` |
| Per-class lock | `synchronized (MyClass.class)` |

### When instance is better

| Avoid static | Prefer |
|--------------|--------|
| Mutable global counters | Injected service / DI bean |
| Unit test doubles | Interface + instance mock |
| Per-request state | Request-scoped object |

### Testing static (Java)

```java
// Prefer refactor to instance
// Or Mockito inline mockStatic (last resort — brittle)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `NullPointerException` on static call | Uninitialized static in cycle | Fix class init order; lazy holder idiom |
| Tests flaky order-dependent | Static mutable state leaks | Reset in `@AfterEach` or remove static |
| "Override" static — wrong method runs | Hiding not overriding | Call via correct type or make instance method |
| Memory leak in app server | Static holds ClassLoader ref | Clear static caches on undeploy |
| Race on static lazy init | Unsynchronized check-then-act | `synchronized` or enum singleton |

## Gotchas

> [!WARNING]
> **Static mutable state** — global variable in disguise; breaks parallel tests and multi-tenant isolation.

> [!WARNING]
> **Don't change meaning per instance** — static fields aren't polymorphic; `Child.staticField` hides `Parent.staticField` — two separate variables.

> [!WARNING]
> **Android context in static** — classic memory leak (`static Activity`); use `Application` context carefully.

> [!WARNING]
> **Initialization order** — static blocks referencing other classes can throw `ExceptionInInitializerError` — hard to debug.

## When NOT to use

- **Dependency injection targets** — Spring/CDI beans should be instances for test/replace.
- **Simulating polymorphism** — static methods don't participate in virtual dispatch.
- **Per-object configuration** — use instance fields.

## Related

[[java]] [[kotlin]] [[method shadowing]] [[Design pattern]]
