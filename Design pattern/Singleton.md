[[Design pattern]] [[Design pattern/Private Properties and Methods]]

# Singleton

> Singleton guarantees one shared instance of a class — private constructor, static accessor, and careful handling of concurrency and test resets.

## Mental model

**Say it in one breath:** Hide the constructor, cache one instance in a static field or closure, and return that instance from `getInstance()`.

### Patterns

1. **Private constructor** — blocks direct `new`; only the class can instantiate itself.
2. **Static property** — holds the single instance (drawback: instance reference may be public).
3. **Closure rewrite** — replaces constructor to return cached instance (drawback: loses prototype additions between definition and rewrite).

```javascript
function Universe() {
  let instance;
  Universe = function () {
    return instance;
  };
  Universe.prototype = this;
  instance = new Universe();
  instance.constructor = Universe;
  return instance;
}
```

```javascript
var Universe;
(function () {
  let instance;
  Universe = function () {
    if (instance) return instance;
    // initialize once
    instance = this;
    return instance;
  };
})();
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Multiple instances in tests | Shared static state | Add `resetInstance()` for test isolation |
| Race in multithreaded code | Lazy init without lock | Eager init or synchronized accessor |
| Hidden global state | Singleton used everywhere | Inject dependency instead |

## Gotchas

> [!WARNING]
> **Singleton is global mutable state** — hard to test and reason about in large codebases.

> [!WARNING]
> **TypeScript `public` constructor** — allows multiple instances unless you make the constructor `private`.

## When NOT to use

- **Dependency injection containers** — prefer scoped services over static singletons.
- **Stateless utilities** — plain functions need no instance.

## Related

[[Design pattern]] [[Design pattern/Private Properties and Methods]] [[LLD/Questions/Logger]]
