[[Design pattern]] [[Design pattern/Singleton]] [[Design pattern/Factory Method]]

# Dependency Injection

> Dependency Injection supplies a component's dependencies from outside rather than letting it construct them — so behavior stays testable and wiring stays explicit.





## Interview Relevance
DI questions test invert-control — constructor injection, test doubles, and avoiding hidden service locators.

## Sources
- Martin, *Dependency Injection* principles (commonly cited in enterprise patterns) — overview

## Key Concepts
Without injection:

```text
class Service { db = new PostgresDatabase() }  // hard-coded
```

With injection:

```text
class Service { constructor(db: Database) { this.db = db } }
```

The **injector** (framework, main function, or factory) chooses `PostgresDatabase` vs `InMemoryDatabase`.

## Technical Details
**Injection styles**

| Style | How dependencies arrive |
|-------|-------------------------|
| **Constructor** | Required deps in constructor (preferred) |
| **Setter** | Optional or late-bound deps |
| **Interface / method** | Dependencies passed per call |

Constructor injection makes required dependencies visible and immutable.

**Relation to patterns**

- Replaces many [[Design pattern/Singleton]] uses with scoped instances.
- Works with [[Design pattern/Factory Method]] and [[Design pattern/Creation pattern/Abstract Factory]] at the composition root.
- Frameworks (Spring, NestJS, Angular) automate binding interfaces to implementations.

## Real-World Applications
- Unit tests need mocks/fakes.
- Multiple deployments (cloud vendor A vs B) share business logic.
- Libraries that should not choose global configuration.

## Comparison
**vs Service Locator**

Service Locator hides `get("Database")` inside the class — looks like flexibility but obscures dependencies. Injection makes the contract explicit in the type signature.

## Mistakes to Avoid
- Constructor with dozens of parameters — split classes (violates SRP) or use facades.
- Container magic without understanding the graph — failures at runtime instead of compile time (less of an issue in statically typed languages).
