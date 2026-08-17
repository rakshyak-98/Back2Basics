[[Design pattern]] [[Design pattern/Singleton]] [[Design pattern/Factory Method]]

# Dependency Injection

> Dependency Injection supplies a component's dependencies from outside rather than letting it construct them — so behavior stays testable and wiring stays explicit.

```txt
        Dependency Injecti ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Interview Relevance
- **Interview probes:** DI questions test invert-control

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

- **Note:** The **injector** (framework, main function, or factory) chooses `PostgresData…

## Technical Details
- **Injection styles:** 

| Style | How dependencies arrive |
|-------|-------------------------|
| **Constructor** | Required deps in constructor (preferred) |
| **Setter** | Optional or late-bound deps |
| **Interface / method** | Dependencies passed per call |

- Constructor injection makes required dependencies visible and immutable.

- **Relation to patterns:** 

- Replaces many [[Design pattern/Singleton]] uses with scoped instances.
- Works with [[Design pattern/Factory Method]] and [[Design pattern/Creation pa…
- Frameworks (Spring, NestJS, Angular) automate binding interfaces to implement…

## Mistakes to Avoid
- **Mistake:** Constructor with dozens of parameters
- **Mistake:** Container magic without understanding the graph

## Comparison
- **vs Service Locator**

- Service Locator hides `get("Database")` inside the class


### Use cases
- Unit tests need mocks/fakes.
- Multiple deployments (cloud vendor A vs B) share business logic.
- Libraries that should not choose global configuration.
