[[Multi-tier and Layered Architecture]] [[presentation layer]] [[Service Layer]] [[frontend layered architecture]] [[SOLID]] [[Design pattern/Dependency Injection]] [[Design pattern/Adapter]] [[KISS]] [[Orchestration layer]] [[DRY]] [[Microservice]] [[gRPC]] [[API design]] [[React Architecture]]

# Clean Architecture

> Clean Architecture — keep business rules independent of frameworks by pointing all source dependencies inward.

```txt
        Clean Architecture ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Clean Architecture interviews test the Dependency Rule

## Sources
- [Robert C. Martin — Clean Architecture (blog)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) — deep-dive
- [Alistair Cockburn — Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) — overview

## Key Concepts
- **Note:** Clean Architecture is a **dependency-management** pattern, not a deployment d…

```txt
        ┌──────────────────────────────────────────┐
- **Note:** │ Frameworks & Drivers (DB, web, UI, SDK) │ ◄── details / mechanisms
        ├──────────────────────────────────────────┤
        │  Interface Adapters  (controllers,        │
- **Note:** │ presenters, gateways, repo impl) │ ◄── format conversion
        ├──────────────────────────────────────────┤
- **Note:** │ Use Cases (application-specific rules) │ ◄── orchestrates per goal
        ├──────────────────────────────────────────┤
- **Note:** │ Entities (enterprise / critical rules) │ ◄── innermost policy
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

- **Note:** **Control flow versus compile-time deps:** A use case may *call* a database (…

- **Note:** **Martin's five properties** of a well-architected system ([Ch

1. Independent of frameworks
2. Testable without UI, DB, or web server
3. Independent of UI
4. Independent of database
5. Independent of external agencies

## Technical Details
### Decision table: when Clean Architecture earns its cost

| Signal | Lean toward Clean | Lean toward simpler layering / [[KISS]] |
|--------|-------------------|----------------------------------------|
| Domain complexity | Rich invariants, rules change independently of infra | Pure CRUD, no business rules |
| Lifespan | Multi-year product, multiple teams | Prototype, throwaway, weekend MVP |
| Testability need | Must unit-test rules without DB/UI | Integration tests sufficient |
| Interface count | Web + CLI + batch + events share core | Single REST API |
| Infra volatility | Expect DB/framework swaps | Stack locked for project life |
| Team size | Boundaries prevent stepping on each other | Solo dev, < 3 engineers |

- **Martin's bar:** Earn structure when **testability and longevity** justify ~…
- Victor Rentea's pragmatic simplifications ([blog](https://victorrentea.ro/blo…

### Lineage (what Clean Architecture synthesizes)

- Martin explicitly credits prior work.
- These patterns share the same goal

| Pattern | Author | Year | Emphasis |
|---------|--------|------|----------|
| **BCE** (Boundary-Control-Entity) | Ivar Jacobson | 1992 | Use-case-driven OO; boundary objects mediate actors |
| **Hexagonal / Ports & Adapters** | Alistair Cockburn | 2005 | Symmetry of driving vs driven sides; "hexagon" is diagram convenience ([source](https://alistair.cockburn.us/hexagonal-architecture)) |
| **Onion Architecture** | Jeffrey Palermo | 2008 | More concentric rings; domain model innermost ([part 1](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)) |
| **Screaming Architecture** | Robert C. Martin | 2011 | Folder structure should scream **use cases**, not frameworks ([blog](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html)) |
| **DCI** (Data, Context, Interaction) | James Coplien & Trygve Reenskaug | 2009 | Runtime role injection for behavior vs data separation |
| **Clean Architecture** | Robert C. Martin | 2012 blog / 2017 book | Unified concentric diagram + Dependency Rule as the single invariant |

- In practice, teams often use "Clean Architecture" as an umbrella term.
- The **invariant** across all of them: protect the core from volatile outer de…

### The four rings (typical layers)

- Circles are **schematic** — you may need more than four.
- The Dependency Rule always applies regardless of ring count.

### 1. Entities (innermost)

- **Enterprise-wide or application-wide critical business rules.:** Most stable

- Can be objects with methods, or plain data + functions
- Hold **invariants** ("account balance cannot go negative", "order total must …
- Zero imports from outer layers
- In a single-application context without an enterprise, entities = the applica…

- **Not:** anemic structs with all logic pushed to a "service god class".
- Entities should enforce critical rules

### 2. Use Cases (application business rules)

- **Application-specific operations:** 

- Orchestrate entities; coordinate data flow in and out
- Define **outbound port interfaces** (e.g., `OrderRepository`, `PaymentGateway…
- Isolated from DB schema, UI framework, and HTTP response types
- Change when **application operations** change

- Examples: `TransferMoney`, `RegisterUser`, `PlaceOrder`, `CancelSubscription`.

- Maps closely to the [[Service Layer]] in traditional layering

### 3. Interface Adapters

- Convert between **use-case-friendly** formats and **external-agency** formats.

| Adapter type | Examples | Direction |
|--------------|----------|-----------|
| **Driving (primary)** | REST controllers, gRPC handlers, CLI commands, message consumers | Outside → in |
| **Driven (secondary)** | Repository implementations, email senders, payment API clients, presenters | In → outside |
| **Presenters** | Format use-case output for a specific UI/API contract | Outbound from use case |

- MVC lives **here**: controllers, views, presenters
- **All SQL:** restricted to repository adapters in this ring (if using SQL)
- Repository **interface** is owned by use cases

### 4. Frameworks & Drivers (outermost)

- Glue to volatile details: Express, Spring, Postgres driver, React, Kafka clie…
- **Minimal code:** 

- Martin's repeated mantra ([No DB](https://blog.cleancoder.com/uncle-bob/2012/…

### The Dependency Rule (the invariant)

> Source code dependencies can only point **inward**. Nothing in an inner circle can know anything about an outer circle — including names of functions, classes, variables, or any named entity. — Martin

| Inner layer | Must NOT |
|-------------|----------|
| **Entities** | Import use cases, controllers, ORM, HTTP |
| **Use cases** | Import SQL drivers, web frameworks, concrete repo impls |
| **Adapters** | Push framework types inward across boundaries |
| **Any inner ring** | Use data formats generated by outer frameworks (e.g., ORM row objects, `gin.Context`) as use-case parameters |

- **Data crossing boundaries:** Only **simple data structures**
- Never pass ORM entities, DB row objects, or HTTP request objects inward.
- Map at the adapter edge.

```txt
  Controller ──► UseCase ──► Entity
       │              │
       │              └── calls IOrderRepository (interface, inner)
       │                        ▲
       │                        │ implements
       └── depends on ──► PostgresOrderRepository (adapter, outer)
```

### Crossing boundaries: Dependency Inversion in practice

- When a use case must call outward (save to DB, send HTTP response), the inner…

```txt
Use Case                    Interface Adapters
────────                    ──────────────────
CreateOrderInteractor  ──►  IOrderRepository (port, defined HERE)
       │                         ▲
       │                         │ implements
       └──► Order (entity)   PostgresOrderRepository
```

- Same pattern for presenters: use case calls `CreateOrderOutputPort` (interfac…

- **Composition root:** (`main.ts`, `cmd/server`, DI module) is the only place t…

```typescript
// composition root — outermost wiring
const repo = new PostgresOrderRepository(pool);
const useCase = new CreateOrderInteractor(repo);
const controller = new CreateOrderController(useCase);
```

- See [[Design pattern/Dependency Injection]] for wiring patterns and test doub…

### Screaming Architecture

> *"The architecture of a software application should scream about the use cases of the application."* — [Martin, 2011](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html)

| Weak (framework-screaming) | Strong (domain-screaming) |
|----------------------------|---------------------------|
| `controllers/`, `models/`, `views/` | `createorder/`, `enrollstudent/`, `billing/` |
| "It's a Rails app" | "It's an accounting / streaming / healthcare system" |
| New hire asks "where are use cases?" | Use cases visible in top-level package names |

- Good architecture **defers** framework and DB decisions.
- You should be able to deliver as console application, web application, or thi…

### Comparison: Clean vs Hexagonal vs Onion

| Aspect | Hexagonal (Cockburn) | Onion (Palermo) | Clean (Martin) |
|--------|---------------------|-----------------|----------------|
| **Diagram** | Hexagon with ports on edges | Concentric rings | Concentric circles |
| **Core emphasis** | Symmetry of driving/driven adapters | Domain model innermost; more rings | Entities + use cases as inner policy |
| **Terminology** | Ports & adapters | Domain services, application services, infrastructure | Entities, use cases, interface adapters, frameworks |
| **Shared invariant** | Dependencies point inward | Dependencies point inward | **Dependency Rule** — source deps inward only |
| **Practical difference** | Mostly naming/diagram | Extra rings for domain/application services | Explicit "what data crosses boundaries" rules |

- All three produce similar folder structures in production code.
- Pick one vocabulary per team and enforce the Dependency Rule

### Standard structure / code

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

- Frontend analogue: [[frontend layered architecture]]

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

- If business-rule tests require Docker, the Dependency Rule is already violate…

### Triage (design review / when architecture breaks)

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

## Mistakes to Avoid
- **Mistake:** **Clean Architecture ≠ microservices.** Each service is usually …
- **Mistake:** **The database is not the center.** Martin ([No DB](https://blog…
- **Mistake:** **Pass-through layers are worse than no layers.** Adapters that …
- **Mistake:** **DTO mapping fatigue.** Not every transition needs a new type
- **Mistake:** **MVC `Model` ≠ Entity.** In Clean Architecture, MVC models are …
- **Mistake:** **Discipline erodes under deadline pressure.** One `import` of a…

## Pros/Cons or Trade-offs
- **Trade-off:** **Pragmatic path:** Start with simple layered monolith (handler → service → repository). Extract ports and use-case packages when tests fight Docker, rules outlive framework churn, or a second delivery channel appears. Easier to add boundaries later than delete empty ones.
