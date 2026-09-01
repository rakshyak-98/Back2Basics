
Condensed from *Dive Into Design Patterns* (Shvets, Refactoring.Guru) and the project standard in [design-patterns.md](design-patterns.md).

**Difference between the two documents:** `design-patterns.md` is binding for *this* codebase. This file is portable — recall material for any Java/Spring project. Nothing here is project-specific.

---

## 1. The four principles (everything else is downstream)

| Principle | One-line test |
|---|---|
| **Encapsulate what varies** | Does a business-rule change force me to edit a conditional? Then the varying part isn't isolated. |
| **Program to an interface** | Do I name a concrete class where I only need a capability? |
| **Favor composition over inheritance** | Are there ≥2 independent axes of variation? Inheritance can only express one. |
| **SRP** | Can I name two different reasons this class would change? |
| **OCP** | Does adding a case mean *adding a class*, or *editing a method*? |

> Using these principles mindlessly can cause more harm than good. — p. 51

---

## 2. The 22 patterns in one line each

### Creational — *how objects get made*
| Pattern | Intent |
|---|---|
| Factory Method | Superclass defines creation; subclasses choose the concrete type. |
| Abstract Factory | Create *families* of related objects without naming concrete classes. |
| Builder | Construct a complex object step by step; same steps, different representations. |
| Prototype | Copy existing objects without depending on their classes. |
| Singleton | One instance, global access point. |

### Structural — *how objects are assembled*
| Pattern | Intent |
|---|---|
| Adapter | Make an incompatible interface usable. |
| Bridge | Split abstraction from implementation into two hierarchies that vary independently. |
| Composite | Treat a tree of objects as if it were one object. |
| Decorator | Add behavior by wrapping, stackably. |
| Facade | One simple interface over a complex subsystem. |
| Flyweight | Share common state so more objects fit in memory. |
| Proxy | Stand in for another object and control access to it. |

### Behavioral — *how responsibility is assigned*
| Pattern | Intent |
|---|---|
| Chain of Responsibility | Pass a request along handlers; each processes or forwards. |
| Command | Turn a request into an object — queue it, log it, undo it. |
| Iterator | Traverse a collection without exposing its structure. |
| Mediator | Components talk through a hub instead of to each other. |
| Memento | Snapshot and restore state without exposing internals. |
| Observer | Publish events to subscribers who registered interest. |
| State | Behavior changes with internal state; looks like the object changed class. |
| Strategy | Interchangeable algorithms behind one interface. |
| Template Method | Fixed algorithm skeleton; subclasses fill in steps. |
| Visitor | Move an operation out of the object hierarchy it acts on. |

---

## 3. Discriminations — the part that's actually hard

Every pair below has near-identical UML. The difference is *intent*, and intent is what gets asked about and what gets designed wrong.

### State vs Strategy
Same structure: a context delegating to an interface.
- **Strategy** — implementations are *mutually ignorant*. The **client** picks one. Answers *"how should this be done?"*
- **State** — states *know about each other* and **trigger their own transitions**. The object drives itself. Answers *"what can happen next?"*
- Book, p. 358: "the particular states may be aware of each other and initiate transitions from one state to another, whereas strategies almost never know about each other."

### Strategy vs Template Method
- **Strategy** — composition. Swappable at runtime. Replaces the *whole* algorithm.
- **Template Method** — inheritance. Fixed at compile time. Replaces *steps* inside a fixed skeleton.
- Prefer Strategy: inheritance couples subclass to superclass internals and locks you to one axis.

### Adapter vs Facade
- **Adapter** — an interface *already exists* and is wrong for you. You conform to a required interface.
- **Facade** — you invent a *new, simpler* interface because the subsystem is complex.
- Rule of thumb: Adapter is usually forced on you; Facade is a choice.

### Adapter vs Decorator vs Proxy (all three wrap)
| | Interface | Purpose | Stackable? |
|---|---|---|---|
| **Adapter** | **Changes** it | Compatibility | No |
| **Decorator** | **Keeps** it | Adds behavior | Yes — that's the point |
| **Proxy** | **Keeps** it | Controls access / lifecycle | Rarely |

Decorator and Proxy are structurally identical. Decorator *enhances*; Proxy *guards, defers, or caches*. A Decorator is normally given its wrappee; a Proxy usually creates or manages it.

### Factory Method vs Abstract Factory vs Builder
- **Factory Method** — one product, type chosen by subclass. A single method.
- **Abstract Factory** — a *family* of products that must be used together (all-Windows widgets, all-Mac widgets). An object with several methods.
- **Builder** — one product, but construction has *many steps and options*. Cares about the *process*; returns the product at the end.

### Observer vs Mediator
- **Observer** — one-to-many *broadcast*. Publisher doesn't know or care who listens. Unidirectional.
- **Mediator** — many-to-many *coordination*. The mediator knows all participants and orchestrates them.
- Mediator is often *implemented using* Observer. They're not alternatives so much as different scales.

### Composite vs Decorator
Both are recursive wrappers.
- **Composite** — has *many* children; the point is uniform treatment of leaf and branch.
- **Decorator** — has *exactly one* child; the point is adding behavior.

### Chain of Responsibility vs Decorator
Both pass through a chain.
- **CoR** — a handler may **stop** the chain. Handling is conditional.
- **Decorator** — every wrapper **always** delegates onward. Nobody gets to abort.

### Command vs Strategy
- **Strategy** — a choice of algorithm, swapped in.
- **Command** — a *request* with its parameters captured as an object, so it can be queued, retried, logged, or undone. If you need a history or a queue, it's Command.

---

## 4. Smell → pattern (the reverse index)

This is how the patterns actually get selected in practice: you notice a smell, not a pattern.

| What you see in the code | Reach for |
|---|---|
| `switch`/`if-else` on a **type code** | Strategy, or plain polymorphism |
| `switch` on a **state field**, plus transition assignments | State |
| The same conditional repeated across several methods | State |
| Adding a business rule means **editing** an existing method | Strategy or Chain of Responsibility (OCP) |
| Ordered validations/checks that can each abort | Chain of Responsibility |
| Telescoping constructors, many optional params | Builder |
| `new ConcreteThing()` inside business logic | Factory / dependency injection |
| Caller must invoke 5 objects in the right order | Facade |
| A third-party model leaking into domain code | Adapter |
| Cross-cutting logging / caching / retry added by editing methods | Decorator, or AOP |
| Combinatorial subclass explosion (A×B×C) | Bridge, or plain composition |
| Everything depends on everything | Mediator |
| Need undo, replay, audit, or a queue of actions | Command |
| Need snapshot / rollback of object state | Memento |
| One object's change must notify several others | Observer |
| Adding an operation means touching every class in a hierarchy | Visitor |
| Class does three unrelated things | None — just extract collaborators (SRP) |

---

## 5. Spring already implements these — using GoF instead is a defect

Portable across any Spring project. **Check this list before writing a pattern.**

| Pattern | Spring's version |
|---|---|
| Singleton | Default bean scope. Never hand-roll — it hides deps in static state and kills testability. |
| Prototype | `@Scope("prototype")` |
| Factory | The container itself; `@Bean` methods, `ObjectProvider`, `FactoryBean` |
| Abstract Factory | Inject `Map<String, T>` or `List<T>` of beans and select |
| Proxy | AOP — `@Transactional`, `@Cacheable`, `@Async`, `@Retryable`, `@PreAuthorize` |
| Decorator *(cross-cutting)* | AOP aspects. Keep GoF Decorator for **domain** wrapping only. |
| Observer | `ApplicationEventPublisher` + `@EventListener` / `@TransactionalEventListener` |
| Strategy | Inject `List<T>` / `Map<String,T>`, select by a `supports()` method |
| Chain of Responsibility | `List<T>` + `@Order`; or servlet `Filter` / `HandlerInterceptor` |
| Template Method | `JdbcTemplate`, `RestTemplate` — Template Method + callback, in the name |
| Adapter | `HandlerAdapter`, `HttpMessageConverter`, `Converter<S,T>` |
| Builder | Lombok `@Builder`; `WebClient.builder()`, `RestClient.builder()` |
| Command | `Runnable`/`Callable`, `@Async`, `ApplicationRunner` |
| Iterator | JDK `Iterable` / `Stream` |

**Two Spring-specific traps worth memorizing:**
1. `@Transactional` and `@Async` work by proxy — **self-invocation bypasses them**. Calling `this.method()` inside the same bean skips the proxy entirely and the annotation silently does nothing.
2. Event listeners should use `@TransactionalEventListener(phase = AFTER_COMMIT)` for side effects, and publish **IDs, not JPA entities** — a detached entity in an async listener throws `LazyInitializationException`.

---

## 6. Decision heuristics

- **Rule of Three.** Two occurrences may be coincidence; three is a pattern. Don't abstract on the second.
- **Gate 0 — does the framework already do it?** If yes, stop. This kills more bad designs than any other rule.
- **Gate 1 — is anything actually varying?** One implementation and no second one planned = ceremony, not abstraction.
- **Name the axis of variation in one sentence.** If you can't, you don't have one and you're pattern-matching on shape.
- **YAGNI beats OCP for unproven axes.** OCP is worth paying for where change is *demonstrated*, not imagined.
- **Composition by default.** Inheritance only for a genuine is-a with a single axis of variation.
- **Patterns are vocabulary before they are code.** "This is a chain of validators" communicates faster than any diagram — the naming benefit is real even when the implementation is trivial.
- **The cost is indirection.** Every pattern trades a direct call for a lookup. Pay it when variation is real; refuse it when it isn't.

> Speculative flexibility is a cost with no offsetting benefit.

---

## 7. Anti-patterns of pattern use

Recognize these in your own work and in review:

1. **Pattern cargo-culting** — copying the UML diagram instead of applying the principle. The book's diagrams assume no DI container and no ORM; yours has both.
2. **Interface-per-class reflex** — an interface with one implementation forever. Justify it by proxying or test doubles, or delete it.
3. **Framework duplication** — hand-rolled Singleton, Factory, or Proxy in a Spring codebase. §5.
4. **Premature Visitor / Bridge** — high-machinery patterns applied to a domain model that's still moving.
5. **Abstraction without a second case** — the most common one. Gate 1 exists to catch it.
6. **Pattern name as justification** — "it's a Strategy" is not a reason. The reason is the axis of variation it isolates.

---

## 8. Fastest path to recall

If you revisit only one thing, make it **§3 (discriminations)** and **§4 (smell → pattern)**. Section 2 is a lookup table you'll never need to memorize; sections 3 and 4 are the reasoning you can't look up in the moment.

Order to study: §1 principles → §4 smells → §3 discriminations → §5 Spring → §6 heuristics.
