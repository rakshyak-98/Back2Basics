[[SOLID]] [[DRY]] [[API design]] [[System design]]

# GRASP

> GRASP (General Responsibility Assignment Software Patterns) guides which object should own a behavior — answering "who should know this?" and "who should create that?" before [[SOLID]] shapes the type relationships.





## Interview Relevance
Name several GRASP patterns (Information Expert, Controller, Low Coupling) and apply them to a class-responsibility sketch.

## Sources
- Craig Larman, *Applying UML and Patterns* (Prentice Hall, 3rd ed.) — GRASP patterns — overview
- Robert C. Martin, *Clean Architecture* — controllers and use-case boundaries — overview

## Key Concepts
- **Information Expert:** put behavior with the data that knows.
- **Creator / Controller:** who creates objects; who handles system events.
- **Low Coupling / High Cohesion:** change isolation and focused modules.
- **Polymorphism / Pure Fabrication:** vary by type; invent service objects when needed.


### Design pass (lightweight)

```txt
1. List use cases or domain events
2. Assign a Controller per use case entry
3. Place business rules on Information Experts
4. Create new instances near their Creator / Expert
5. Extract Pure Fabrications for email, database, payment software development kits
```

### Smells

| Smell | GRASP lens |
|-------|------------|
| God service class | Split Controllers and Experts |
| Domain imports Simple Mail Transfer Protocol software development kit | Pure Fabrication gateway |
| Enum switch in ten places | Polymorphism / Strategy |
| Cannot test without database | Creator and coupling — inject factories |

## Technical Details
### Core patterns

Craig Larman documented GRASP in *Applying UML and Patterns*. The patterns are questions, not ceremony:

| Pattern | Question | Typical answer |
|---------|----------|----------------|
| **Information Expert** | Who has the data needed for this rule? | Put behavior on the object that already holds the facts |
| **Creator** | Who should instantiate this object? | Aggregator that contains or closely uses the new instance |
| **Controller** | Who handles this system event or use case? | Application-layer coordinator (not only HTTP controller) |
| **Low Coupling** | How do we minimize dependencies? | Depend on interfaces; avoid god imports |
| **High Cohesion** | Are responsibilities related? | Split classes that change for unrelated reasons |
| **Polymorphism** | Where is `switch (type)`? | Replace with subtype polymorphism |
| **Pure Fabrication** | No domain object fits this technical role? | Gateway, repository, notifier — invented for indirection |
| **Indirection** | Two classes too tightly coupled? | Introduce mediator between them |
| **Protected Variations** | What is likely to change? | Stable interface around volatile implementation |

## Real-World Applications
OO responsibility assignment in domain models and service layers.

## Pros/Cons or Trade-offs
- **Pro:** Shared vocabulary for design critiques.
- **Con:** Cargo-cult pattern names without force.
- **Trade-off:** more indirection vs direct scripts.

## Comparison
GRASP assigns **responsibilities** at design time. SOLID refines **type structure** (substitutability, interface size, dependency direction). Both apply at module boundaries in [[System design]].

Avoid **ManagerFactoryBuilder** over-fabrication — not every line needs a new class.


- vs [[SOLID]]: SOLID is dependency/form; GRASP is responsibility placement.
- vs [[KISS]]: pick the lightest GRASP move that clarifies ownership.

## Mistakes to Avoid
- Skipping failure modes until production.
- Ignoring idempotency, timeouts, or rollback where required.
- Optimizing or distributing before measuring the real bottleneck.
