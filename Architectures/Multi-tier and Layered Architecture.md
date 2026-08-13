[[Clean Architecture]] [[presentation layer]] [[Service Layer]] [[frontend layered architecture]] [[Database application]] [[Microservice]] [[Orchestration layer]] [[SOLID]] [[KISS]]

# Multi-tier and Layered Architecture

> Tiers are where code runs; layers are how code is organized — keep them separate.

---

## How it works

Multi-level architecture is two orthogonal axes:

```txt
                    PHYSICAL (tiers)
                    ─────────────────────────────────────►
                    1-tier    2-tier      3-tier         n-tier
                         ┌─────────┐  ┌────┬────┐  ┌───┬───┬───┬───┐
  LOGIC (layers)         │ UI+logic│  │UI  │ DB │  │UI │API│BL │DB │
  inside one deployable  │ + DB    │  │+log│    │  │   │GW │SVC│   │
                         └─────────┘  └────┴────┘  └───┴───┴───┴───┘
```

| Term      | Separated by                                     | Question it answers          |
| --------- | ------------------------------------------------ | ---------------------------- |
| **Tier**  | Process, machine, network, security zone         | *Where does this run?*       |
| **Layer** | Package, module, namespace, dependency direction | *Who may call whom in code?* |

**Strict versus relaxed layering:** In a **strict** layered system, layer *N* talks only to layer *N−1*. In a **relaxed** system, upper layers may skip intermediate layers (faster to build, harder to change). Most production code is relaxed — document which skips are allowed.

**Dependency rule (Martin / hexagonal / clean):** Source dependencies point **inward** only — toward higher-level **policies**. Outer rings (HTTP, DB, queues) depend on inner rings (use cases, entities) — never the reverse. Flow of control can go outward; compile-time deps cannot. Crossing that gap uses **Dependency Inversion** ([[SOLID]] DIP): inner layer defines the interface (port); outer layer implements it (adapter).

**Martin's core thesis:** Architecture is about **managing dependencies so the system survives change** — not about picking Spring, Postgres, or microservices. Frameworks, the web, and the database are **details** to keep at the outer edge.

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| "Works in Postman, wrong in UI" | Client doing business logic (2-tier leak) | Move rules to [[Service Layer]]; UI displays only |
| Schema change breaks mobile app | Fat client queries DB or embeds SQL | API versioning; server-owned contract |
| Random data corruption | Handler writes DB without transaction | Wrap multi-table updates in service txn ([[ACID]]) |
| Can't unit test without Docker | Domain imports ORM/HTTP types | Introduce ports (Martin DIP); in-memory adapters for tests |
| ORM models used as domain entities | `@Entity` annotations in "domain" package | Separate entity from persistence model; map at adapter boundary |
| DB row / `ResultSet` passed to use case | Framework data structure crossed inward | Map to simple DTO in repository adapter before returning |
| Folder layout says "Spring" not "Billing" | Framework-screaming structure | Reorganize by use case (Screaming Architecture — see below) |
| 15-hop sync chain, cascading timeouts | N-tier / microservice sprawl | Merge services or go async; [[backpressure]] |
| "Distributed monolith" — must deploy all 12 together | Shared DB, shared libs, circular calls | Database-per-service; define bounded contexts |
| Layer violation in PRs | Controller imports repository directly | Enforce module boundaries (archunit, eslint boundaries) |
| Gateway does business logic | BFF/gateway grew fat | Push rules to domain services; gateway routes/auth only |
| Performance fine in dev, slow in prod | Extra network tier not in local compose | Measure p99 per hop; colocate or cache |
| Team argues "3-tier vs microservices" | Conflating physical and logical | Draw two diagrams: deployment + module deps |

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
> **Tiers ≠ layers.** A team that "went to microservices" but kept one shared database and synchronous chains still has a **distributed monolith** — worst of both worlds.

> [!WARNING]
> **Skipping the service layer** — controllers that call repositories directly bypass validation, authz, and transactions. First shortcut becomes permanent.

> [!WARNING]
> **Framework dictates folder structure** — Martin: frameworks are tools, not architecture. `controllers/models/views` layout defers use-case discovery; structure should scream domain operations.

> [!WARNING]
> **Database row crosses boundary** — passing ORM/query result objects into use cases violates the Dependency Rule; map to plain DTOs in the adapter.

> [!WARNING]
> **Anemic domain model** — entities are structs with getters; all logic in services. Martin puts **critical rules in entities**; use cases orchestrate, not replace, entity behavior.

> [!WARNING]
> **Hexagonal on a todo app** — ports/adapters for `TodoRepository`, `ClockPort`, `UuidPort` adds ceremony without boundary value. Use [[KISS]] until complexity earns structure.

> [!WARNING]
> **2-tier security illusion** — "only our app talks to the DB" — if the app ships DB credentials or RLS is weak, users own your data plane.

> [!WARNING]
> **Relaxed layering without documentation** — repository calls another service's HTTP API from the data layer. Debugging requires full stack traces across "layers."

> [!WARNING]
> **N-tier for resume-driven design** — API gateway + BFF + mesh + 6 services for 100 RPS. Operate what you draw; every box needs on-call.

---


## When not to use

| Pattern | Skip when |
|---------|-----------|
| **N-tier / microservices** | Team < 5, no independent scale profiles, no clear bounded contexts ([[KISS]]) |
| **Hexagonal / clean** | Short-lived CRUD, throwaway prototype, single developer |
| **2-tier (thick client)** | Rules must be centrally enforced; multiple client platforms |
| **Separate DAL tier** | Modern pools/ORM in app tier suffice; DAL-as-service adds latency |
| **Strict layering** | Hot path proven by profiling to need layer skip — document exception |

**Rule of thumb:** Default to **3-tier deployment + layered (or hexagonal) monolith**. Split tiers and services when you have **measured** pain: deploy frequency, scale shape, blast radius, or compliance boundary — not because the diagram looks enterprise.

---


## Decision table: which model when?

| Situation | Start with | Evolve to |
|-----------|------------|-----------|
| MVP, < 10k users, small team | **Layered monolith** (3 logical layers, 1–3 tiers) | Extract hot paths |
| Regulated domain, long product life | **Hexagonal monolith** | Services at proven seams |
| Mobile + web different APIs | 3-tier + **BFF** layer | Not separate microservices per screen |
| Independent scale (GPU encode vs API) | **N-tier / microservices** | [[Microservice]] boundaries |
| Offline desktop / embedded | **1-tier** + logical layers | — |
| Internal admin + public API | **3-tier** + network segmentation | Gateway tier |

### Layers vs tiers — common combinations

| Physical tiers | Logical layers | Example |
|----------------|----------------|---------|
| 1 | 4 (layered) | Spring Boot monolith: controller→service→repo→DB in one JVM |
| 3 | 4 | Classic Rails/Django/nginx → app → Postgres |
| 3 | 4 per service | E-commerce: 8 microservices, each internally layered |
| 1 | 4 (hexagonal) | CLI tool with ports for file system and clock |

---


## Standard config / structure

### Minimal 3-tier web (reference layout)

```txt
deploy/
  web/          # tier 1 — static + reverse proxy (nginx)
  api/          # tier 2 — stateless app replicas (horizontally scaled)
  data/         # tier 3 — managed RDS / Cloud SQL (no public IP)

api/src/
  handlers/     # presentation (HTTP)
  services/     # business logic + transactions
  domain/       # entities, rules (optional but valuable)
  repos/        # data access
```

### Layer boundary in code (Go sketch)

```go
// handler — maps HTTP only
func (h *OrderHandler) Create(w http.ResponseWriter, r *http.Request) {
    var req CreateOrderDTO
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil { ... }
    order, err := h.orders.Create(r.Context(), req.ToCommand())
    ...
}

// service — transaction + rules
func (s *OrderService) Create(ctx context.Context, cmd CreateOrderCommand) (Order, error) {
    return s.db.WithTx(ctx, func(tx Tx) (Order, error) {
        if err := s.inventory.Reserve(tx, cmd.SKU, cmd.Qty); err != nil { return Order{}, err }
        return s.orders.Insert(tx, cmd)
    })
}
```

### Hexagonal package layout (Martin-aligned)

```txt
# Screaming architecture — use cases visible at top level
createorder/
  CreateOrderInteractor.ts    # use case (application rules)
  CreateOrderRequest.ts       # simple input DTO
  IOrderRepository.ts         # outbound port (interface)
  entities/Order.ts           # entity (critical rules)

adapters/
  in/web/CreateOrderController.ts   # driving adapter
  out/persistence/PostgresOrderRepository.ts  # driven adapter — ALL SQL here

# Anti-pattern (framework-screaming):
# controllers/ models/ views/  ← tells you Rails/MVC, not what the app DOES
```

### Scaling knobs per tier

| Tier | Scale lever | Watch |
|------|-------------|-------|
| Presentation | CDN, edge cache, static offload | Cache invalidation, auth on edge |
| Application | Horizontal pods, stateless design | Session stickiness, [[connection pooling]] |
| Data | Read replicas, sharding ([[database sharding]]) | Replica lag, cross-shard queries |
| Gateway | Rate limits ([[Token bucket]]), autoscale | Single point of misconfiguration |

---


## Physical tiers (deployment models)

### 1. Single-tier (1-tier)

All concerns — UI, business logic, data — run in **one process on one machine**.

| Example | Notes |
|---------|-------|
| Desktop app + embedded SQLite | Classic 1-tier |
| Mobile app with on-device Room/Core Data | Logical layers possible; still 1 physical tier |
| Single Docker container running UI+API+Postgres | 1-tier *deployment* even if code has 4 layers |

**When it fits:** Offline-first, edge devices, prototypes, low-latency local tools.

### 2. Two-tier (client–server)

Client owns **presentation + application logic**; server owns **data** (database or file server).

```txt
[ Thick client: UI + business rules ] ──SQL/ODBC──► [ Database server ]
```

| Pros | Cons |
|------|------|
| Simple topology | Business rules duplicated per client (fat client) |
| Low server CPU | Schema change forces client redeploy |
| | Hard to enforce invariants — client can bypass rules |
| | Connection credentials often on every laptop |

**Modern echo:** SPA + direct Supabase/Firebase from browser is a **2-tier anti-pattern** unless Row Level Security and server-side rules fully enforce policy.

### 3. Three-tier (most common web pattern)

| Tier | Responsibility | Typical tech |
|------|----------------|--------------|
| **Presentation** | UI, HTTP termination, input validation (format) | Browser, CDN, static assets |
| **Application / business** | Rules, orchestration, authz, transactions | App servers, BFF, API |
| **Data** | Persistence, integrity, backup | RDBMS, object store |

```txt
Browser ──HTTPS──► App server(s) ──TCP──► Database
   (tier 1)           (tier 2)            (tier 3)
```

**Why it won:** Each tier scales and patches independently; DB never exposed to the internet; business rules live in one place.

**Typical production layout:** Web tier in DMZ → application tier on private subnet → DB tier with no outbound internet. Firewall between each hop ([[Security group]] patterns).

### 4. N-tier (extended physical separation)

Splits the 3-tier model for **scale, security, or team boundaries**:

```txt
Client → CDN/Edge → API Gateway → BFF → Microservices → DAL → DB/Cache/Queue
```

| Extra tier | Why split |
|------------|-----------|
| **API / Gateway** | Auth, rate limit, routing, TLS, WAF — one front door |
| **BFF (Backend for Frontend)** | Mobile vs web DTO shapes without polluting core services |
| **Service / microservice tier** | Independent deploy, blast-radius isolation |
| **Data access tier** | Shared read/write path, connection pooling service (rare as separate tier today) |
| **Async / worker tier** | [[kafka]] consumers, batch jobs — off hot request path |

**Cost:** Every new tier adds network hops, failure modes, distributed tracing needs, and deployment coordination. N-tier is a **scaling and org tool**, not a maturity badge.

---


## Logical layers (inside one deployable)

Layers exist **inside** a monolith, microservice, or mobile application. Two common models — do not conflate them.

### Traditional layered (top-down call stack)

```txt
┌─────────────────────────────────────────────┐
│  Controller / Handler  (HTTP, gRPC, CLI)      │
├─────────────────────────────────────────────┤
│  Service               (orchestration, txn) │
├─────────────────────────────────────────────┤
│  Domain / Entity       (rules, invariants)    │
├─────────────────────────────────────────────┤
│  Repository / DAO      (queries, mapping)     │
└─────────────────────────────────────────────┘
         │ call direction (runtime) ──► DB
```

**Canonical flow:** [[presentation layer]] → [[Service Layer]] → Repository → DB. See [[Database application]] for transaction boundaries.

| Layer | Owns | Must NOT |
|-------|------|----------|
| **Controller/Handler** | Protocol mapping, status codes, DTO ↔ domain | SQL, business rules, direct DB |
| **Service** | Use cases, transactions, multi-repo orchestration | HTTP headers, ORM entities leaking upward |
| **Domain** | Entities, value objects, domain services, invariants | `import` from web/DB SDKs |
| **Repository/DAO** | Queries, mapping rows ↔ domain | Business policy ("can user withdraw?") |

### Clean Architecture (Martin — dependency direction inward)

→ Full reference: [[Clean Architecture]] (layers, Dependency Rule, DIP, lineage, code sketches, design-review triage).

Martin organizes by **policy stability**, not call order. Inner = most abstract; outer = mechanisms/details.

```txt
        ┌──────────────────────────────────────────┐
        │  Frameworks & Drivers  (DB engine, web)   │  ◄── details
        ├──────────────────────────────────────────┤
        │  Interface Adapters  (controllers,        │
        │    presenters, gateways, repo impl)       │  ◄── converts formats
        ├──────────────────────────────────────────┤
        │  Use Cases  (application-specific rules)   │  ◄── orchestrates entities
        ├──────────────────────────────────────────┤
        │  Entities  (enterprise / critical rules)   │  ◄── innermost policy
        └──────────────────────────────────────────┘
              ▲ compile-time deps point IN only
```

| Martin ring | Responsibility | Stability |
|-------------|----------------|-----------|
| **Entities** | Critical business rules; usable across apps in an enterprise | Highest — unaffected by UI, DB, or page navigation changes |
| **Use cases** | Application-specific rules; orchestrate entities per user goal | Changes when app operations change — not when DB or framework changes |
| **Interface adapters** | Convert data between use-case format and external format (HTTP, SQL rows, message payloads) | Changes when delivery mechanism changes |
| **Frameworks & drivers** | Glue to Spring, Express, Postgres, Kafka — minimal code here | Most volatile — "the web is a detail; the database is a detail" |

**Key Martin corrections versus traditional layered:**

| Traditional habit | Martin's rule |
|-------------------|---------------|
| Repository is a layer *below* domain | Repository **interface** (port) lives with use cases; **implementation** is an outer adapter |
| Controller is "above" everything | Controller is an **interface adapter** — depends inward on use cases |
| Pass ORM entity / DB row into service | Pass **simple DTOs or primitives** across boundaries — never framework-generated row structures inward |
| MVC `Model` holds business logic | MVC models are often **dumb data passed to use cases**; critical rules live in **entities** |
| Folder named `controllers/`, `models/`, `views/` | **Screaming architecture** — folders named for **use cases** (`CreateOrder/`, `EnrollStudent/`) |

**Frontend analogue:** [[frontend layered architecture]] — presentation / application / domain / infrastructure folders.

### Strict call rules (design review checklist)

```txt
Traditional layered (runtime flow):
  ✓ Handler → Service → Repository → DB
  ✗ Handler → Repository (skips rules)

Martin Clean Architecture (compile-time deps):
  ✓ Adapter → Use Case → Entity
  ✓ Use Case defines IOrderRepository; PostgresOrderRepository implements it (outer)
  ✗ Entity imports @Entity, gin.Context, sql.Row
  ✗ Use case imports SQL driver or HTTP response types
  ✗ Pass ORM model or DB row structure inward across a boundary
```

---


## Hexagonal / Clean Architecture (ports and adapters)

Martin unified Hexagonal (Cockburn), Onion (Palermo), and related patterns under one idea: **separation of concerns via layers + the Dependency Rule**. Same goal as traditional layering, but organized as **concentric rings** with explicit **ports** (interfaces) and **adapters** (implementations).

### Martin's five properties of a good architecture

A system built this way should be ([Clean Architecture, Ch. 22](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)):

1. **Independent of frameworks** — use frameworks as tools; don't let them dictate structure
2. **Testable** — business rules testable without UI, DB, or web server
3. **Independent of UI** — swap web UI for CLI without touching business rules
4. **Independent of database** — swap Postgres for Mongo without touching entities/use cases
5. **Independent of external agencies** — business rules know nothing about the outside world

### Ports, adapters, and boundary crossing

```txt
         ┌──────── REST adapter (primary/driving)
         │         flow of control ──►
    ┌────┴────────────────────────────────────┐
    │  PORT: CreateOrderUseCase (inbound)      │
    │  ┌────────────────────────────────────┐  │
    │  │  ENTITIES: Order, Money             │  │
    │  │  USE CASE: CreateOrderInteractor    │  │
    │  └────────────────────────────────────┘  │
    │  PORT: OrderRepository (outbound)         │  ◄── interface defined HERE
    └────┬────────────────────────────────────┘
         │         source code deps ──► inward
         └──────── PostgresOrderRepository (adapter — outer)
```

| Concept | Meaning |
|---------|---------|
| **Port** | Interface the **inner layer defines** — use case declares `IOrderRepository`; presenter output port for responses |
| **Adapter** | Outer class that **implements** the port — Postgres repo, REST controller, email sender |
| **Primary (driving)** | Outside world initiates — HTTP controller, CLI, message consumer |
| **Secondary (driven)** | App initiates outward — DB write, payment API, notification |
| **Dependency rule** | Adapters depend on ports; entities and use cases never depend on adapters |
| **DIP at boundaries** | When use case must call presenter/repo, it calls an **interface in its own layer**; outer class implements it — deps oppose flow of control |

**What crosses boundaries:** Only **simple data structures** — structs, DTOs, function arguments, plain maps. Never pass entities tied to outer frameworks, and never pass **database row structures** inward (Martin's explicit anti-pattern).

### Screaming Architecture (Martin)

> *"The architecture of a software application should scream about the use cases of the application."* — [Screaming Architecture](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html)

| Screams frameworks (weak) | Screams domain (Martin-aligned) |
|---------------------------|----------------------------------|
| `controllers/`, `models/`, `views/` | `createorder/`, `enrollstudent/`, `processpayment/` |
| "It's a Rails app" | "It's a health-care / accounting / streaming system" |
| New hire asks "where are the use cases?" | New hire finds use cases in top-level package names |

Good architecture **defers** framework, DB, and web-server decisions. You should be able to deliver as console application, web application, or thick client without rewriting core policy.

**Payoff:** Domain tests without containers; swap Postgres for in-memory; change REST to gRPC by new adapter only; frameworks become replaceable details.

**Cost:** ~2–3× more types/files; overkill for CRUD with 5 tables and one developer. Martin's bar: earn the structure when **testability and longevity** justify it.

---


## Microservices (distribution-level multi-tier)

Microservices are **not** a replacement for layers — each service is usually a **small layered or hexagonal application** deployed independently.

```txt
                    DISTRIBUTION (between services)
                    ───────────────────────────────────►

  Service A                    Service B
  ┌──────────────┐            ┌──────────────┐
  │ handler      │   HTTP/    │ handler      │
  │ service      │◄─event────►│ service      │
  │ repository   │            │ repository   │
  └──────┬───────┘            └──────┬───────┘
         │                           │
         ▼                           ▼
       DB A                         DB B
```

| Pattern | Coordinator | When |
|---------|-------------|------|
| **Sync (REST/gRPC)** | Caller blocks | Simple query chains, < 3 hops |
| **Async (events)** | [[kafka]] / queue | Decouple, absorb spikes |
| **Saga orchestration** | [[Orchestration layer]] (Temporal, etc.) | Multi-step with compensation |

See [[Microservice]] (streaming boundaries) and [[KISS]] — don't split before failure domains justify it.

---


## Validation: Robert C. Martin alignment

Cross-check any design against Martin's *Clean Architecture* ([blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), book Ch. 20–22). This note's tier/layer content is **compatible** when applied as below.

### Alignment matrix

| This note teaches | Martin agrees | Caveat |
|-------------------|---------------|--------|
| Tiers ≠ layers | Yes — physical deployment is orthogonal to dependency structure | 3-tier deploy does not imply clean inner deps |
| Dependency rule (inward only) | Yes — central rule | Must hold at **source code** level, not just diagram |
| Entities vs use cases | Yes — two inner rings with different stability | Don't collapse both into a generic "service layer" |
| Controllers/repos as adapters | Yes — Interface Adapters + Frameworks rings | SQL belongs in adapter, not "domain repository layer" |
| Ports and adapters | Yes — Martin credits Cockburn; same DIP mechanism | Port interface owned by inner layer |
| Microservices as distribution | Yes — with caution | Martin warns against premature distribution; each service still needs clean internal deps |
| Testability without infra | Yes — primary payoff of the rule | If you need Docker to unit-test rules, deps point wrong way |
| Web/DB/framework as details | Yes — defer and isolate | BFF/gateway are fine; business rules must not live there |
| Screaming architecture | Yes — use-case-first structure | Added explicitly in this note |
| Traditional Handler→Service→Repo | Partial | Valid **runtime** flow; map Service→**Use Case**, ensure **compile-time** deps still point inward |
| Anemic domain as gotcha | Yes — entities should carry critical rules | Use cases orchestrate; entities enforce invariants |
| Default to layered monolith | Yes — Martin favors monolith until boundaries proven | "Monolith" must still respect Dependency Rule |

### Martin pass/fail checklist (design review)

```txt
PASS when:
  □ Entities compile with zero framework/DB imports
  □ Use cases depend on entity + port interfaces only
  □ All SQL/HTTP/SDK code lives in outer adapters
  □ Tests run business rules without DB, web server, or container
  □ Top-level packages/folders name use cases or domain areas
  □ Data crossing boundaries is plain DTOs — not ORM rows
  □ Swapping Postgres → in-memory needs only adapter rewrite

FAIL when:
  □ "Domain" package imports JPA, ActiveRecord, or axios
  □ Use case accepts HttpRequest or sql.Rows as parameters
  □ Architecture diagram is only deployment boxes (tiers) with no dependency diagram
  □ Framework chosen on day 1 dictated all folder names
  □ Microservices split before use cases and entities are stable in a monolith
```

### Where Martin would push back on common industry practice

| Industry habit | Martin's view |
|----------------|---------------|
| "We're 3-tier so we're well-architected" | Deployment shape ≠ dependency hygiene |
| Shared ORM models across services | Each service owns its entities; integrate via API/events, not shared tables |
| Fat gateway/BFF with business rules | Rules belong in use cases; gateway routes/auth/transforms only |
| Repository as a sub-layer under domain in UML | Port with inner interface, outer implementation |
| DDD aggregate = JPA `@Entity` | Persistence model is an adapter concern; map to/from entity |

**Bottom line:** Multi-tier answers *where* components run. Martin's Clean Architecture answers *which direction code is allowed to depend*. A correct system needs both diagrams — and they are independent.

---


## Related

**Layers in this vault:** [[Clean Architecture]] · [[presentation layer]] · [[Service Layer]] · [[frontend layered architecture]] · [[Database application]] · [[Orchestration layer]]

**Distribution & scale:** [[Microservice]] · [[distributed system]] · [[database sharding]] · [[stateless]] · [[event-driven]]

**Principles:** [[SOLID]] · [[KISS]] · [[DRY]] · [[Design pattern/Dependency Injection]]

**Martin / Clean Architecture:** [The Clean Architecture (blog)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) · [Screaming Architecture (blog)](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html) · *Clean Architecture* (Robert C. Martin, 2017)

**APIs between tiers:** [[gRPC]] · [[API design]] · [[HTTP module]]

## Sources

- [Wikipedia — Multi-tier and Layered Architecture](https://en.wikipedia.org/wiki/Multi-tier_and_Layered_Architecture)
