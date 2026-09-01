**Source of authority:** *Dive Into Design Patterns*, Alexander Shvets (Refactoring.Guru, v2023-2.46) — 22 GoF patterns, plus the design-principles framework in its opening chapters.

This document is the **decision procedure** for low-level design in this codebase. It exists so that "which pattern do we use here?" has a repeatable answer instead of a per-developer one, and so that the far more common right answer — *no pattern* — is defensible rather than lazy.

The book's own warning is the frame for everything below:

> Using these principles mindlessly can cause more harm than good. The cost of applying these principles into a program's architecture might be making it more complicated than it should be. — *SOLID Principles*, p. 51

---

## 1. The decision procedure

Apply these gates **in order**. Stop at the first one that resolves the question. Most questions resolve at Gate 0 or 1.

| Gate | Question | If yes |
|---|---|---|
| **0. Does the framework already do it?** | Is Spring, JPA, or the JDK already providing this pattern? | **Stop.** Use the framework. See §5 (Rejected). |
| **1. Is anything actually varying?** | Do we have ≥2 real implementations *today*, or a scheduled second one? | If no — write the direct code. Revisit when the second case is real. |
| **2. What varies?** | Name the axis of change in one sentence. | The axis determines the category (§2). |
| **3. Category** | Creation / structure / behavior? | Pick from the catalog in §3. |
| **4. Cost check** | Does the pattern add more indirection than the variation costs? | If yes — inline it and leave a comment naming the pattern you rejected. |

Gate 1 is the one that gets skipped. The book is explicit that flexibility has a price:

> After making this change, you won't probably feel any immediate benefit. On the contrary, the code has become more complicated than it was before. — *Program to an Interface*, p. 43

Speculative flexibility is a cost with no offsetting benefit. Pay it when the second implementation is real.

---

## 2. The prior questions (principles before patterns)

Every pattern in the catalog is a packaged application of one of these four ideas. If you cannot name which one you are applying, you are pattern-matching on shape rather than solving a problem.

### 2.1 Encapsulate What Varies
> Identify the aspects of your application that vary and separate them from what stays the same. (p. 38)

The book's worked example is *literally our domain*: a `getOrderTotal` method with tax rules baked into conditionals, extracted first to a method, then to a `TaxCalculator` collaborator. Our pricing code faces the same pressure (§4, **D2**).

**Test for this repo:** if a `switch`/`if-else` chain branches on an enum or a country/channel/tier code, and a new business rule means editing that chain — the varying part is not encapsulated.

### 2.2 Program to an Interface, not an Implementation
> Depend on abstractions, not on concrete classes. (p. 42)

The book's four-step recipe:
1. Determine what one object needs from the other — which methods does it call?
2. Describe those methods in a new interface or abstract class.
3. Make the dependency implement that interface.
4. Make the consumer depend on the interface.

**Caveat for this repo:** an interface with exactly one implementation and no second one planned is ceremony, not abstraction. Our `UserService`/`UserServiceImpl` pair is currently that — justified only because Spring AOP proxying and test doubles benefit from it. Do not extend the habit to every class reflexively.

### 2.3 Favor Composition Over Inheritance
> Inheritance ... represents the "is a" relationship; composition represents the "has a" relationship. (p. 48)

The book's combinatorial-explosion example (cargo type × engine type × navigation type → an unmanageable subclass lattice, p. 49) is exactly the trap waiting in a booking engine, where the axes are **service type × pricing rule × cancellation policy × payment method**. Four axes crossed by inheritance is a class explosion. Four axes composed is four small interfaces.

**Rule for this repo:** booking behavior varies along independent axes. Those axes get composed as injected collaborators, never as an entity subclass hierarchy.

### 2.4 SOLID — the two that carry the weight here
The book lists all five (pp. 51–70). Two do the real work in a Spring service layer:

- **SRP** — a class changes for one reason. Our `BookingServiceImpl` currently changes when booking rules change, *and* when DTO shape changes, *and* when booking-number format changes. Three reasons, three responsibilities.
- **OCP** — open for extension, closed for modification. Adding a new pricing rule or a new validation must mean *adding a class*, not editing a chain of conditionals. This is the criterion that most often selects Strategy or Chain of Responsibility.

LSP, ISP and DIP matter, but in a DI-container codebase DIP is largely satisfied by constructor injection and ISP by keeping service interfaces small. Do not write a document section justifying them; just do not violate them.

---

## 3. Pattern selection map — booking domain

The book's 22 patterns, mapped to the concerns that actually arise in this system. Status column is binding; rationale is in §4 and §5.

### Creational — *object creation mechanisms* (p. 72)

| Pattern | Book's intent | Our concern | Status |
|---|---|---|---|
| **Factory Method** | Interface for creating objects in a superclass, subclasses alter the type | Payment gateway / notification channel instantiation | **Deferred** — Spring container is our factory (§5) |
| **Abstract Factory** | Families of related objects without specifying concrete classes | Per-region supplier client families | **Deferred** — no second family yet |
| **Builder** | Construct complex objects step by step | `Booking` construction with many optional fields | **Adopted via Lombok `@Builder`** (D7) |
| **Prototype** | Copy objects without depending on their classes | Recurring / duplicated bookings | **Deferred** — revisit for "repeat this booking" |
| **Singleton** | One instance, global access point | — | **Rejected** (§5) |

### Structural — *assembling objects into larger structures* (p. 147)

| Pattern | Book's intent | Our concern | Status |
|---|---|---|---|
| **Adapter** | Let incompatible interfaces collaborate | Third-party supplier/channel-manager APIs | **Adopt on first integration** (D6) |
| **Bridge** | Split abstraction from implementation into two hierarchies | Booking type × fulfilment backend | **Deferred** — one backend today |
| **Composite** | Tree structures treated as individual objects | Package bookings containing sub-bookings | **Adopt when packages ship** (D10) |
| **Decorator** | Attach behaviors via wrapper objects | Cross-cutting concerns (audit, cache, retry) | **Rejected** in favour of Spring AOP (§5) |
| **Facade** | Simplified interface to a complex subsystem | Payment orchestration; AWS SDK surface | **Adopt** (D5) |
| **Flyweight** | Share common state to fit more objects in RAM | — | **Rejected** — not a memory-bound system |
| **Proxy** | Substitute controlling access to another object | Caching, lazy loading, access control | **Rejected** — Spring AOP / `@Cacheable` (§5) |

### Behavioral — *algorithms and assignment of responsibilities* (p. 247)

| Pattern | Book's intent | Our concern | Status |
|---|---|---|---|
| **Chain of Responsibility** | Pass a request along handlers, each decides to process or pass on | Booking validation pipeline | **Adopt now** (D3) |
| **Command** | Turn a request into a stand-alone object; queue, delay, undo | Async jobs, SQS message payloads | **Adopt for SQS work** (D9) |
| **Iterator** | Traverse a collection without exposing its representation | — | **Rejected** — JDK provides it |
| **Mediator** | Restrict direct communication; objects collaborate via a mediator | Cross-service coordination | **Deferred** — events cover it (D4) |
| **Memento** | Save/restore previous state without exposing internals | Booking amendment history / rollback | **Deferred** — audit table covers it today |
| **Observer** | Subscription mechanism notifying objects about events | Booking lifecycle side effects | **Adopt via Spring events** (D4) |
| **State** | Alter behavior when internal state changes | Booking status lifecycle | **Adopt now — highest priority** (D1) |
| **Strategy** | Family of interchangeable algorithms | Pricing, cancellation, payment | **Adopt now** (D2) |
| **Template Method** | Algorithm skeleton in superclass, subclasses override steps | Shared booking-flow scaffolding | **Constrained** — prefer Strategy (§5) |
| **Visitor** | Separate algorithms from the objects they operate on | Reporting over booking trees | **Deferred** — premature |

---

## 4. Ratified decisions

### D1 — State: the booking lifecycle *(adopt now, highest priority)*

**The book's applicability test** (p. 365): use State when an object behaves differently depending on its current state; when a class is polluted with massive conditionals keyed on a field; when there is duplicated code across transitions of a condition-based state machine.

**Our situation is the degenerate case of that test.** `Booking` has six states and `BookingServiceImpl.updateBookingStatus` currently accepts *any* transition between them:

```java
// BookingServiceImpl.java — current
booking.setStatus(status);   // CANCELLED -> CONFIRMED is accepted. So is COMPLETED -> PENDING.
```

There are no conditionals to extract because the invariants were never written. The transition table exists only in people's heads. That is worse than the book's "monstrous conditionals" starting point, because the bugs are silent.

**Decision — two stages, deliberately.**

*Stage 1 (now):* put the transition table in the enum. A JPA-persisted entity and a polymorphic state-object graph fight each other; Hibernate wants a column, GoF State wants an object reference. Encoding legality in the enum gets the invariant enforced without that fight:

```java
public enum BookingStatus {
    PENDING    { public Set<BookingStatus> next() { return EnumSet.of(CONFIRMED, CANCELLED); } },
    CONFIRMED  { public Set<BookingStatus> next() { return EnumSet.of(IN_PROGRESS, CANCELLED, RESCHEDULED); } },
    IN_PROGRESS{ public Set<BookingStatus> next() { return EnumSet.of(COMPLETED, CANCELLED); } },
    RESCHEDULED{ public Set<BookingStatus> next() { return EnumSet.of(CONFIRMED, CANCELLED); } },
    COMPLETED  { public Set<BookingStatus> next() { return EnumSet.noneOf(BookingStatus.class); } },
    CANCELLED  { public Set<BookingStatus> next() { return EnumSet.noneOf(BookingStatus.class); } };

    public abstract Set<BookingStatus> next();
    public boolean canTransitionTo(BookingStatus t) { return next().contains(t); }
}
```

…enforced in one place on the entity, so no service can bypass it:

```java
// Booking.java
public void transitionTo(BookingStatus target) {
    if (!status.canTransitionTo(target)) {
        throw new IllegalStateTransitionException(bookingNumber, status, target);
    }
    this.status = target;
}
```

*Stage 2 (trigger-based):* promote to full GoF State classes — `BookingState` interface with `confirm()`, `cancel()`, `complete()` — **when** per-state behavior diverges beyond transition legality. Concretely: when cancellation fees differ by state, or when confirmation side effects differ by state. Until then Stage 2 is indirection without payoff (Gate 4).

Note this is the enum-as-state-machine idiom, not textbook GoF State. That is deliberate and it is the book's own advice applied rather than its diagram copied.

### D2 — Strategy: pricing *(adopt now)*

**The book's distinction from State** (p. 358): strategies almost never know about each other; states may. Pricing rules are mutually ignorant. Strategy, not State.

**Our situation:** `totalAmount` arrives from the client in `BookingDTO` and is persisted unchallenged. That is both a design gap and a trust boundary violation — the caller sets the price. Server-side computation is mandatory, and the moment it exists it will vary by service type, season, tier and channel. Four axes: exactly the composition case from §2.3.

```java
public interface PricingStrategy {
    boolean supports(BookingRequest request);
    Money price(BookingRequest request);
}
```

Spring injects every implementation; selection is by `supports`, so a new rule is a new `@Component` and no edit to existing code (OCP):

```java
@Service
@RequiredArgsConstructor
public class PricingService {
    private final List<PricingStrategy> strategies;   // Spring collects all beans

    public Money priceFor(BookingRequest request) {
        return strategies.stream()
            .filter(s -> s.supports(request))
            .findFirst()
            .orElseThrow(() -> new NoPricingRuleException(request))
            .price(request);
    }
}
```

Order with `@Order` when rules overlap. Apply the same shape to **cancellation policy** and **payment method** — the other two axes.

### D3 — Chain of Responsibility: booking validation *(adopt now)*

**The book's motivating example is our exact problem** (p. 252): an online ordering system where a request must pass a series of sequential checks, each able to abort the rest, and where the set of checks grows over months.

Our checks: availability, blackout dates, lead time, user eligibility, duplicate detection, payment pre-authorization. These are ordered, each can reject, and the list will grow.

```java
public interface BookingValidator extends Ordered {
    void validate(BookingRequest request);   // throws BookingValidationException to abort
}
```

Spring's `List<BookingValidator>` injection with `@Order` gives the chain without hand-wiring `next` pointers. A validator is added by adding a class — never by editing a validation method.

**Why not one `validate()` method with six `if` blocks:** that method changes for six unrelated reasons (SRP), and every new rule edits shared code (OCP).

### D4 — Observer: domain events *(adopt — via Spring, not hand-rolled)*

Booking confirmation must trigger: confirmation email, SMS, analytics, SQS publication, cache invalidation. Wiring these into `BookingServiceImpl` couples booking rules to notification infrastructure and makes the service change whenever a new side effect appears.

**Do not implement Observer.** Spring's `ApplicationEventPublisher` *is* Observer, with transaction-bound delivery we would otherwise have to build:

```java
publisher.publishEvent(new BookingConfirmedEvent(booking.getId(), booking.getBookingNumber()));

@TransactionalEventListener(phase = AFTER_COMMIT)
public void onConfirmed(BookingConfirmedEvent event) { /* send email */ }
```

`AFTER_COMMIT` matters: side effects must not fire for a transaction that rolls back. A hand-rolled Observer would not give us that.

**Publish IDs, not entities.** A detached JPA entity in an async listener is a `LazyInitializationException` waiting to happen.

### D5 — Facade: payment orchestration *(adopt)*

A payment involves gateway auth, fraud check, ledger write, receipt generation. Callers should see one method. The book: *provides a simplified interface to a library, a framework, or any other complex set of classes* (p. 148).

`PaymentFacade.charge(BookingId, Money)` — one entry point, subsystem hidden. Also apply to the AWS SDK surface: our `AWSConfig` currently exposes four raw SDK clients as beans. Wrap the ones we use (`S3Client`, `SqsClient`) behind intention-revealing interfaces — `DocumentStore`, `EventQueue` — so the SDK is swappable and mockable in tests.

### D6 — Adapter: external supplier APIs *(adopt on first integration)*

The book's Adapter case (p. 151) is a third-party library expecting a different data format than ours. Every channel manager, GDS and supplier we integrate will have its own model. Each gets an adapter implementing our port interface; **no external DTO reaches the domain layer.** This is the boundary that keeps a supplier's schema change from becoming a domain change.

### D7 — Builder: keep Lombok, do not hand-roll *(adopted)*

`@Builder` is already on our entities and DTOs and satisfies the book's intent — step-by-step construction of an object with many optional fields. A hand-written GoF Builder with a separate `Director` adds classes and buys nothing here. Revisit only if we need *different representations* from the same construction sequence, which is the part of Builder's intent Lombok does not cover.

### D8 — MapStruct for mapping *(adopt now)*

`mapToDTO` is currently a hand-written private method duplicated across `UserServiceImpl` and `BookingServiceImpl`. It is a second responsibility inside a service class (SRP) and it silently rots when a field is added. MapStruct is **already a declared dependency and an annotation processor in `pom.xml`, and is entirely unused.** Generate the mappers; delete the hand-written ones.

### D9 — Command: asynchronous work *(adopt for queued jobs)*

The book: *turns a request into a stand-alone object ... lets you queue a request's execution* (p. 247). SQS payloads are commands whether or not we name them so. Model them as explicit serializable command objects with a single handler each, rather than passing loose maps. This makes retries, dead-lettering and replay tractable.

### D10 — Composite: package bookings *(adopt when packages ship)*

A package booking (flight + hotel + transfer) that must be priced, confirmed and cancelled as a unit is the book's tree-of-objects-treated-uniformly case. Do not build it before the requirement is real — but design `Booking` now so a parent/child relation can be added without a rewrite. That is the only anticipatory concession in this document, and it is cheap.

---

## 5. Explicitly rejected — and why

This section exists because the most expensive design mistakes in a Spring codebase come from applying GoF patterns the framework already implements. Rejecting them is a decision, not an omission.

| Pattern | Why rejected here |
|---|---|
| **Singleton** | Spring beans are singleton-scoped by default. A hand-rolled Singleton hides dependencies in static state, defeats constructor injection, and cannot be substituted in tests. The container gives us the lifecycle guarantee without the global-state cost. **Never write one.** |
| **Factory Method / Abstract Factory** | The Spring container *is* our factory. `@Bean` methods and `@Component` scanning cover our creation needs. Reach for these only for runtime type selection the container genuinely cannot express — and prefer injecting a `Map<String, T>` of beans first. |
| **Proxy** | Spring AOP creates proxies for us. Caching is `@Cacheable`, transactions are `@Transactional`, access control is `@PreAuthorize`. A hand-written proxy duplicates the framework and will not compose with it. |
| **Decorator** | Same reasoning for cross-cutting concerns — use AOP. Decorator remains legitimate for *domain* composition (e.g. stacking price adjustments onto a base rate), where wrapping is the business rule rather than infrastructure. |
| **Iterator** | The JDK's `Iterable`/`Stream` already satisfies the intent. |
| **Flyweight** | Solves a memory-footprint problem we do not have. Our constraints are I/O and database, not object count in RAM. |
| **Template Method** | Constrained, not banned. It buys reuse through inheritance, which §2.3 tells us to avoid by default; subclasses become tightly coupled to superclass internals and we cannot vary two axes at once. Use Strategy unless the algorithm skeleton is genuinely fixed and only leaf steps vary. |
| **Visitor** | Adds double-dispatch machinery that is hard to read, and requires a stable object hierarchy. Our domain model is still moving. Revisit only if reporting over a Composite booking tree becomes real. |

---

## 6. Known design defects in the current codebase

Identified by applying §2 to the existing scaffold. Ordered by severity.

1. **Security — password bug.** `UserServiceImpl.createUser` calls `passwordEncoder.encode(userDTO.getEmail())`. It hashes the **email** as the password. Every account is created with a password equal to its own email address. This is a live authentication bypass and is independent of any pattern decision — fix first.
2. **Trust boundary — client-supplied price.** `totalAmount` is taken from the request DTO and persisted without server-side computation (D2).
3. **Missing invariant — unconstrained status transitions.** Any status may follow any other (D1).
4. **Unhandled parse failures.** `BookingServiceImpl` calls `LocalDateTime.parse` on `String` DTO fields. Malformed input throws `DateTimeParseException`, which `GlobalExceptionHandler` maps to a 500 rather than a 400. Use `LocalDateTime` typed fields with `@JsonFormat`, or handle the exception explicitly.
5. **Duplicated mapping logic.** Hand-written `mapToDTO` in two services; MapStruct configured but unused (D8).
6. **Aggregate boundary crossing.** `BookingServiceImpl` injects `UserRepository` directly to resolve a user. It should depend on `UserService` (or a narrow port), not on another aggregate's persistence.
7. **Eager AWS client construction.** `AWSConfig` instantiates four SDK clients at startup regardless of use, each opening connection pools and requiring credentials. Make them lazy or conditional (D5).

---

## 7. Review checklist

For any PR that adds a class:

- [ ] Which gate in §1 selected this design? If none, why does the class exist?
- [ ] If a pattern was applied — does the framework already provide it (§5)?
- [ ] If a conditional branches on an enum or type code — should this be Strategy or State?
- [ ] If a new business rule required editing an existing method — is OCP violated? Should this be a chain or a strategy?
- [ ] If a new interface has exactly one implementation — is the second one real, or speculative?
- [ ] If inheritance was used — are there two independent axes of variation (§2.3)?
- [ ] Do domain events publish IDs rather than JPA entities (D4)?
- [ ] Are external models kept out of the domain by an adapter (D6)?

---

## 8. Attribution

Patterns, intents and applicability criteria are drawn from *Dive Into Design Patterns* by Alexander Shvets (Refactoring.Guru, 2022). Page references are to the v2023-2.46 PDF. Summaries here are paraphrased for application to this codebase; the book is the authority for the patterns themselves and is worth reading directly before a significant design decision.

Online reference: https://refactoring.guru/design-patterns
