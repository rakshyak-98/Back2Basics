[[Multi-tier and Layered Architecture]] [[presentation layer]] [[Service Layer]] [[frontend layered architecture]] [[SOLID]] [[Design pattern/Dependency Injection]] [[Design pattern/Adapter]] [[KISS]]

# Clean Architecture

> Clean Architecture — a dependency-management pattern, not a deployment diagram. Martin unified Hexagonal (Cockburn), Onion (Palermo), Screaming Architecture, DCI (Coplien/Reenskaug), and BCE (Jacobson) into one actionable

---

## How it works

Clean Architecture is a **dependency-management** pattern, not a deployment diagram. Martin unified Hexagonal (Cockburn), Onion (Palermo), Screaming Architecture, DCI (Coplien/Reenskaug), and BCE (Jacobson) into one actionable rule: **source code dependencies point inward only** — toward higher-level **policies** (business rules), never toward mechanisms (web, DB, frameworks).

```txt
        ┌──────────────────────────────────────────┐
        │  Frameworks & Drivers  (DB, web, UI, SDK)   │  ◄── details / mechanisms
        ├──────────────────────────────────────────┤
        │  Interface Adapters  (controllers,        │
        │    presenters, gateways, repo impl)       │  ◄── format conversion
        ├──────────────────────────────────────────┤
        │  Use Cases  (application-specific rules)   │  ◄── orchestrates per goal
        ├──────────────────────────────────────────┤
        │  Entities  (enterprise / critical rules)   │  ◄── innermost policy
        └──────────────────────────────────────────┘
              ▲ compile-time deps point IN only
              │ runtime control flow may go OUT (via DIP)
```

| Concept | Meaning |
|---------|---------|
| **Policy** | Business rules — what the system *must* do regardless of delivery mechanism |
| **Mechanism** | How it's delivered — HTTP, SQL, Kafka, React, Spring |
| **Dependency Rule** | Inner circles never import, name, or depend on outer circles |
| **DIP at boundary** | Inner layer defines interface (port); outer layer implements (adapter) |
| **Composition root** | Outermost wiring point where concrete adapters are injected ([[Design pattern/Dependency Injection]]) |

**Control flow versus compile-time deps:** A use case may *call* a database (outward control flow), but it calls an **interface it owns**; the Postgres adapter implements that interface. Source deps oppose control flow at boundaries — classic [[SOLID]] Dependency Inversion.

**Martin's five properties** of a well-architected system ([Ch. 22](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)):

1. Independent of frameworks
2. Testable without UI, DB, or web server
3. Independent of UI
4. Independent of database
5. Independent of external agencies

---


## Consequences

**Positive:** …

**Negative / trade-offs:** …


## Alternatives considered

| Alternative | Why rejected |
|-------------|--------------|
| … | … |


## Gotchas

> [!WARNING]
> **Clean Architecture ≠ microservices.** Each service is usually a small hexagonal/clean app internally. Distribution is orthogonal to the Dependency Rule. See [[Multi-tier and Layered Architecture]].

> [!WARNING]
> **The database is not the center.** Martin ([No DB](https://blog.cleancoder.com/uncle-bob/2012/05/15/NODB.html)): letting the DB schema drive design early "warps" use cases. Model use cases first; derive schema from identified queries and relationships.

> [!WARNING]
> **Pass-through layers are worse than no layers.** Adapters that only forward calls add navigation cost with zero boundary value. Every layer must earn its complexity ([Rentea](https://victorrentea.ro/blog/overengineering-in-onion-hexagonal-architectures/), [DEV: Clean Architecture Trap](https://dev.to/marcolenzo/the-clean-architecture-trap-241k)).

> [!WARNING]
> **DTO mapping fatigue.** Not every transition needs a new type. Reuse shapes when identical; map only at real boundary mismatches.

> [!WARNING]
> **MVC `Model` ≠ Entity.** In Clean Architecture, MVC models are often dumb data passed across the adapter ring; critical rules live in entities.

> [!WARNING]
> **Discipline erodes under deadline pressure.** One `import` of an ORM type into a use case starts the leak. Enforce with arch-unit, ESLint `import/no-restricted-paths`, or module boundaries in code review.

---


## When not to use

| Situation | Why skip full Clean Architecture |
|-----------|----------------------------------|
| CRUD API with no business rules | Ports/adapters add ceremony without boundary value |
| Prototype / MVP validation | Time-to-market > long-term isolation |
| Solo dev, short-lived project | Wiring cost exceeds benefit |
| Challenge is ops/scale, not domain rules | Vertical slicing, CQRS, or event-driven may fit better ([Rentea](https://victorrentea.ro/blog/overengineering-in-onion-hexagonal-architectures/)) |
| Every operation is `repository.save(entity)` | Anemic use cases — structure without logic |

**Pragmatic path:** Start with simple layered monolith (handler → service → repository). Extract ports and use-case packages when tests fight Docker, rules outlive framework churn, or a second delivery channel appears. Easier to add boundaries later than delete empty ones.

---


## Decision table: when Clean Architecture earns its cost

| Signal | Lean toward Clean | Lean toward simpler layering / [[KISS]] |
|--------|-------------------|----------------------------------------|
| Domain complexity | Rich invariants, rules change independently of infra | Pure CRUD, no business rules |
| Lifespan | Multi-year product, multiple teams | Prototype, throwaway, weekend MVP |
| Testability need | Must unit-test rules without DB/UI | Integration tests sufficient |
| Interface count | Web + CLI + batch + events share core | Single REST API |
| Infra volatility | Expect DB/framework swaps | Stack locked for project life |
| Team size | Boundaries prevent stepping on each other | Solo dev, < 3 engineers |

**Martin's bar:** Earn structure when **testability and longevity** justify ~2–3× more types/files. Victor Rentea's pragmatic simplifications ([blog](https://victorrentea.ro/blog/overengineering-in-onion-hexagonal-architectures/)): relaxed layers, remove interfaces with only one implementation, merge one-liner pass-through controllers.

---


## Lineage (what Clean Architecture synthesizes)

Martin explicitly credits prior work. These patterns share the same goal — **separation of concerns via inward dependencies** — with different emphasis:

| Pattern | Author | Year | Emphasis |
|---------|--------|------|----------|
| **BCE** (Boundary-Control-Entity) | Ivar Jacobson | 1992 | Use-case-driven OO; boundary objects mediate actors |
| **Hexagonal / Ports & Adapters** | Alistair Cockburn | 2005 | Symmetry of driving vs driven sides; "hexagon" is diagram convenience ([source](https://alistair.cockburn.us/hexagonal-architecture)) |
| **Onion Architecture** | Jeffrey Palermo | 2008 | More concentric rings; domain model innermost ([part 1](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)) |
| **Screaming Architecture** | Robert C. Martin | 2011 | Folder structure should scream **use cases**, not frameworks ([blog](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html)) |
| **DCI** (Data, Context, Interaction) | James Coplien & Trygve Reenskaug | 2009 | Runtime role injection for behavior vs data separation |
| **Clean Architecture** | Robert C. Martin | 2012 blog / 2017 book | Unified concentric diagram + Dependency Rule as the single invariant |

In practice, teams often use "Clean Architecture" as an umbrella term. The **invariant** across all of them: protect the core from volatile outer details via interfaces and inward-pointing dependencies.

---


## The four rings (typical layers)

Circles are **schematic** — you may need more than four. The Dependency Rule always applies regardless of ring count.

### 1. Entities (innermost)

**Enterprise-wide or application-wide critical business rules.** Most stable; least affected by UI, DB, or framework changes.

- Can be objects with methods, or plain data + functions — Martin is explicit either works
- Hold **invariants** ("account balance cannot go negative", "order total must match line items")
- Zero imports from outer layers — no ORM annotations, no HTTP types, no SDK clients
- In a single-application context without an enterprise, entities = the application's core business objects

**Not:** anemic structs with all logic pushed to a "service god class". Entities should enforce critical rules; use cases **orchestrate**, not replace, entity behavior.

### 2. Use Cases (application business rules)

**Application-specific operations** — one class/function per user goal or system operation.

- Orchestrate entities; coordinate data flow in and out
- Define **outbound port interfaces** (e.g., `OrderRepository`, `PaymentGateway`, `NotificationSender`)
- Isolated from DB schema, UI framework, and HTTP response types
- Change when **application operations** change — not when Postgres becomes MongoDB

Examples: `TransferMoney`, `RegisterUser`, `PlaceOrder`, `CancelSubscription`.

Maps closely to the [[Service Layer]] in traditional layering — but in Clean Architecture the service/use-case layer **owns** repository interfaces; implementations live outside.

### 3. Interface Adapters

Convert between **use-case-friendly** formats and **external-agency** formats.

| Adapter type | Examples | Direction |
|--------------|----------|-----------|
| **Driving (primary)** | REST controllers, gRPC handlers, CLI commands, message consumers | Outside → in |
| **Driven (secondary)** | Repository implementations, email senders, payment API clients, presenters | In → outside |
| **Presenters** | Format use-case output for a specific UI/API contract | Outbound from use case |

- MVC lives **here**: controllers, views, presenters — models passed across boundaries are usually **simple DTOs**, not rich entities
- **All SQL** restricted to repository adapters in this ring (if using SQL)
- Repository **interface** is owned by use cases; **implementation** is an adapter

### 4. Frameworks & Drivers (outermost)

Glue to volatile details: Express, Spring, Postgres driver, React, Kafka client. **Minimal code** — mostly configuration and wiring at the **composition root**.

Martin's repeated mantra ([No DB](https://blog.cleancoder.com/uncle-bob/2012/05/15/NODB.html)): *"The database is a detail."* Defer DB and framework decisions until use cases and entities are understood and tested.

---


## The Dependency Rule (the invariant)

> Source code dependencies can only point **inward**. Nothing in an inner circle can know anything about an outer circle — including names of functions, classes, variables, or any named entity. — Martin

| Inner layer | Must NOT |
|-------------|----------|
| **Entities** | Import use cases, controllers, ORM, HTTP |
| **Use cases** | Import SQL drivers, web frameworks, concrete repo impls |
| **Adapters** | Push framework types inward across boundaries |
| **Any inner ring** | Use data formats generated by outer frameworks (e.g., ORM row objects, `gin.Context`) as use-case parameters |

**Data crossing boundaries:** Only **simple data structures** — structs, DTOs, primitives, maps. Never pass ORM entities, DB row objects, or HTTP request objects inward. Map at the adapter edge.

```txt
  Controller ──► UseCase ──► Entity
       │              │
       │              └── calls IOrderRepository (interface, inner)
       │                        ▲
       │                        │ implements
       └── depends on ──► PostgresOrderRepository (adapter, outer)
```

---


## Crossing boundaries: Dependency Inversion in practice

When a use case must call outward (save to DB, send HTTP response), the inner layer defines the contract:

```txt
Use Case                    Interface Adapters
────────                    ──────────────────
CreateOrderInteractor  ──►  IOrderRepository (port, defined HERE)
       │                         ▲
       │                         │ implements
       └──► Order (entity)   PostgresOrderRepository
```

Same pattern for presenters: use case calls `CreateOrderOutputPort` (interface in inner layer); `CreateOrderJsonPresenter` implements it in the adapter ring.

**Composition root** (`main.ts`, `cmd/server`, DI module) is the only place that knows all concrete types:

```typescript
// composition root — outermost wiring
const repo = new PostgresOrderRepository(pool);
const useCase = new CreateOrderInteractor(repo);
const controller = new CreateOrderController(useCase);
```

See [[Design pattern/Dependency Injection]] for wiring patterns and test doubles.

---


## Screaming Architecture

> *"The architecture of a software application should scream about the use cases of the application."* — [Martin, 2011](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html)

| Weak (framework-screaming) | Strong (domain-screaming) |
|----------------------------|---------------------------|
| `controllers/`, `models/`, `views/` | `createorder/`, `enrollstudent/`, `billing/` |
| "It's a Rails app" | "It's an accounting / streaming / healthcare system" |
| New hire asks "where are use cases?" | Use cases visible in top-level package names |

Good architecture **defers** framework and DB decisions. You should be able to deliver as console application, web application, or thick client without rewriting core policy.

---


## Comparison: Clean vs Hexagonal vs Onion

| Aspect | Hexagonal (Cockburn) | Onion (Palermo) | Clean (Martin) |
|--------|---------------------|-----------------|----------------|
| **Diagram** | Hexagon with ports on edges | Concentric rings | Concentric circles |
| **Core emphasis** | Symmetry of driving/driven adapters | Domain model innermost; more rings | Entities + use cases as inner policy |
| **Terminology** | Ports & adapters | Domain services, application services, infrastructure | Entities, use cases, interface adapters, frameworks |
| **Shared invariant** | Dependencies point inward | Dependencies point inward | **Dependency Rule** — source deps inward only |
| **Practical difference** | Mostly naming/diagram | Extra rings for domain/application services | Explicit "what data crosses boundaries" rules |

All three produce similar folder structures in production code. Pick one vocabulary per team and enforce the Dependency Rule — not three competing diagrams.

---


## Standard structure / code

### Package layout (screaming architecture)

```txt
src/
  placeorder/                    # use case as top-level concern
    PlaceOrderInteractor.ts      # application rules
    PlaceOrderRequest.ts         # input DTO (simple struct)
    IOrderRepository.ts          # outbound port
    entities/
      Order.ts                   # critical rules + invariants
  adapters/
    in/web/PlaceOrderController.ts
  out/persistence/PostgresOrderRepository.ts   # ALL SQL here
    out/presenters/PlaceOrderJsonPresenter.ts
  main.ts                        # composition root
```

Frontend analogue: [[frontend layered architecture]] — `domain/` (entities + use cases + port interfaces) with `infrastructure/` implementing repositories.

### TypeScript sketch (minimal)

```typescript
// ── Entity (inner) ──
export class Order {
  constructor(
    readonly id: string,
    private items: OrderLine[],
  ) {}

  addItem(line: OrderLine): void {
    if (line.quantity <= 0) throw new DomainError('quantity must be positive');
    this.items.push(line);
  }

  total(): Money {
    return this.items.reduce((sum, l) => sum.add(l.subtotal()), Money.zero());
  }
}

// ── Port (owned by use case layer) ──
export interface OrderRepository {
  save(order: Order): Promise<void>;
  nextId(): Promise<string>;
}

// ── Use case ──
export class PlaceOrderInteractor {
  constructor(private orders: OrderRepository) {}

  async execute(req: PlaceOrderRequest): Promise<PlaceOrderResponse> {
    const order = new Order(await this.orders.nextId(), []);
    for (const line of req.lines) order.addItem(OrderLine.from(line));
    await this.orders.save(order);
    return { orderId: order.id, total: order.total().amount };
  }
}

// ── Adapter (outer) — maps DB rows ↔ entity, never passes rows inward ──
export class PostgresOrderRepository implements OrderRepository {
  constructor(private pool: Pool) {}
  async save(order: Order): Promise<void> { /* SQL here only */ }
  async nextId(): Promise<string> { /* ... */ }
}
```

### Go sketch

```go
// domain/order.go — entity, no imports from outer packages
type Order struct { ID string; lines []Line }
func (o *Order) AddLine(l Line) error { /* invariant checks */ return nil }

// usecase/place_order.go — port defined here
type OrderRepository interface {
    Save(ctx context.Context, o Order) error
}

type PlaceOrder struct { repo OrderRepository }
func (uc PlaceOrder) Execute(ctx context.Context, cmd PlaceOrderCommand) error {
    var o Order
    // build entity, enforce rules
    return uc.repo.Save(ctx, o)
}

// adapter/postgres/order_repo.go — SQL isolated
type PostgresOrderRepo struct { db *sql.DB }
func (r PostgresOrderRepo) Save(ctx context.Context, o Order) error { /* ... */ }
```

### Testing payoff

```typescript
// unit test — no DB, no HTTP server
const fakeRepo: OrderRepository = {
  save: async () => {},
  nextId: async () => 'ord-1',
};
const result = await new PlaceOrderInteractor(fakeRepo).execute(sampleRequest);
expect(result.total).toBe(42);
```

If business-rule tests require Docker, the Dependency Rule is already violated.

---


## Triage (design review / when architecture breaks)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unit tests need Docker / Testcontainers | Domain or use case imports DB/HTTP SDK | Extract port; inject in-memory adapter in tests |
| ORM `@Entity` in `domain/` package | Framework types crossed inward | Separate persistence model; map at repository adapter |
| `sql.Rows` or ORM model passed to use case | Row structure from outer framework inward | Map to plain DTO in adapter before return |
| Controller calls repository directly | Layer skip; rules bypassed | Route through use case / [[Service Layer]] |
| Use case imports `express.Request` | HTTP detail in application layer | Map to `PlaceOrderRequest` DTO in controller |
| 5 files changed for one field rename | Empty pass-through layers | Collapse ceremony; keep only layers with real logic |
| "Clean" folder tree, anemic entities | Logic in services, entities are getters | Move invariants into entities; use cases orchestrate |
| Interface + impl for every class | Dogmatic abstraction | Keep interface only when ≥2 impls or DIP boundary requires it |
| Can't find use cases in codebase | Framework-screaming layout | Reorganize by use case ([Screaming Architecture](#screaming-architecture)) |
| Microservice shares ORM models | Distributed monolith at data layer | Each service owns entities; integrate via API/events |
| Gateway/BFF contains business rules | Policy leaked to outer tier | Move rules to use cases; gateway routes/auth/transforms only |

### Pass/fail checklist (Martin alignment)

```txt
PASS:
  □ Entities compile with zero framework/DB imports
  □ Use cases depend on entities + port interfaces only
  □ All SQL/HTTP/SDK code in outer adapters
  □ Business-rule tests run without DB, web server, or container
  □ Top-level packages name use cases or domain areas
  □ Data across boundaries = plain DTOs, not ORM rows
  □ Swapping Postgres → in-memory needs only adapter rewrite

FAIL:
  □ "Domain" imports JPA, ActiveRecord, gin, or axios
  □ Use case accepts HttpRequest or sql.Rows
  □ Architecture diagram is deployment-only (tiers) with no dependency diagram
  □ Framework chosen day 1 dictated all folder names
  □ Microservices split before entities/use cases stable in monolith
```

---


## Related

**Vault siblings:** [[Multi-tier and Layered Architecture]] · [[presentation layer]] · [[Service Layer]] · [[frontend layered architecture]] · [[Orchestration layer]]

**Principles & patterns:** [[SOLID]] · [[Design pattern/Dependency Injection]] · [[Design pattern/Adapter]] · [[KISS]] · [[DRY]]

**Distribution:** [[Microservice]] · [[gRPC]] · [[API design]]

**Frontend:** [[frontend layered architecture]] · [[React Architecture]]

---


### References


### Primary sources (Robert C. Martin)

| Resource | URL |
|----------|-----|
| **The Clean Architecture** (blog, Aug 2012) | https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html |
| **No DB** (database as detail) | https://blog.cleancoder.com/uncle-bob/2012/05/15/NODB.html |
| **Screaming Architecture** (Sep 2011) | https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html |
| *Clean Architecture: A Craftsman's Guide to Software Structure and Design* (Prentice Hall, 2017) | ISBN 978-0134494164 |
| InformIT excerpt — Dependency Rule & layers | https://www.informit.com/articles/article.aspx?p=2832399 |

### Lineage & related patterns

| Resource | URL |
|----------|-----|
| Alistair Cockburn — Hexagonal (Ports & Adapters) | https://alistair.cockburn.us/hexagonal-architecture |
| Jeffrey Palermo — Onion Architecture part 1 | https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/ |
| Wikipedia — Hexagonal architecture | https://en.wikipedia.org/wiki/Hexagonal_architecture_(software) |
| Thoughtworks — Demystifying architecture patterns | https://www.thoughtworks.com/insights/blog/architecture/demystify-software-architecture-patterns |
| Growing Object Oriented Software, Guided by Tests (Freeman & Pryce) | Hexagonal in practice |

### Critical / pragmatic perspectives

| Resource | URL |
|----------|-----|
| Victor Rentea — Overengineering in Onion/Hexagonal | https://victorrentea.ro/blog/overengineering-in-onion-hexagonal-architectures/ |
| Marco Lenzo — The Clean Architecture Trap | https://dev.to/marcolenzo/the-clean-architecture-trap-241k |
| Application Architect — Dependency Rule deep dive | https://www.application-architect.com/posts/clean-architecture-dependency-rule-and-layers/ |
| softengbook.org — Clean Architecture chapter | https://softengbook.org/articles/clean-architecture |

### Implementations & examples

| Ecosystem | Resource |
|-----------|----------|
| .NET | Jason Taylor — [Clean Architecture Solution Template](https://github.com/jasontaylordev/CleanArchitecture) |
| Java | Tom Hombergs — *Get Your Hands Dirty on Clean Architecture* (Packt, 2020) |
| Go | Standard library + explicit ports; see `cmd/` as composition root |
| Node/TS | Manual DI at `main.ts`; NestJS modules as composition root (don't let decorators leak inward) |

## Sources

- [Wikipedia — Clean Architecture](https://en.wikipedia.org/wiki/Clean_Architecture)
