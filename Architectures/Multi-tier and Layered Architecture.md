[[presentation layer]] [[Service Layer]] [[frontend layered architecture]] [[Database application]] [[Microservice]] [[Orchestration layer]] [[SOLID]] [[KISS]]

# Multi-tier and Layered Architecture

> **Tiers** = where code runs (physical/deployment). **Layers** = how code is organized (logical/modules). A 3-tier web app can still be a spaghetti monolith inside the middle tier — **Martin, Cockburn, Microsoft App Arch Guide**.

---

## Mental model

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

| Term | Separated by | Question it answers |
|------|--------------|---------------------|
| **Tier** | Process, machine, network, security zone | *Where does this run?* |
| **Layer** | Package, module, namespace, dependency direction | *Who may call whom in code?* |

**Strict vs relaxed layering:** In a **strict** layered system, layer *N* talks only to layer *N−1*. In a **relaxed** system, upper layers may skip intermediate layers (faster to build, harder to change). Most production code is relaxed — document which skips are allowed.

**Dependency rule (hexagonal/clean):** Source dependencies point **inward** only. Outer rings (HTTP, DB, queues) depend on inner rings (use cases, domain) — never the reverse. Flow of control can go outward; compile-time deps cannot.

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

**Typical production layout:** Web tier in DMZ → app tier on private subnet → DB tier with no outbound internet. Firewall between each hop ([[Security group]] patterns).

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

Layers exist **inside** a monolith, microservice, or mobile app. Common stack:

```txt
┌─────────────────────────────────────────────┐
│  Controller / Handler  (HTTP, gRPC, CLI)    │  ← adapters IN
├─────────────────────────────────────────────┤
│  Service / Use case    (orchestration, txn)   │
├─────────────────────────────────────────────┤
│  Domain / Entity       (rules, invariants)    │  ← no framework imports
├─────────────────────────────────────────────┤
│  Repository / DAO      (persistence port)     │
└─────────────────────────────────────────────┘
         ▲                              ▲
         │ implements                 │ implements
   PostgresRepo                  RestController
   (infrastructure)             (infrastructure)
```

| Layer | Owns | Must NOT |
|-------|------|----------|
| **Controller/Handler** | Protocol mapping, status codes, DTO ↔ domain | SQL, business rules, direct DB |
| **Service** | Use cases, transactions, multi-repo orchestration | HTTP headers, ORM entities leaking upward |
| **Domain** | Entities, value objects, domain services, invariants | `import` from web/DB SDKs |
| **Repository/DAO** | Queries, mapping rows ↔ domain | Business policy ("can user withdraw?") |

**Canonical flow:** [[presentation layer]] → [[Service Layer]] → Repository → DB. See [[Database application]] for transaction boundaries.

**Frontend analogue:** [[frontend layered architecture]] — presentation / application / domain / infrastructure folders.

### Strict call rules (design review checklist)

```txt
✓ Handler → Service → Repository → DB
✗ Handler → Repository (skips rules)
✗ Repository → Service (inverted dependency)
✗ Domain imports framework types (@Entity, axios, gin.Context)
```

---

## Hexagonal / Clean Architecture (ports and adapters)

**Same goal as layered**, but organized as **concentric rings** with explicit **ports** (interfaces) and **adapters** (implementations). Names: Hexagonal (Cockburn), Clean (Martin), Onion (Palermo) — shared **dependency rule**.

```txt
         ┌──────── REST adapter (primary/driving)
         │
    ┌────┴────────────────────────────────────┐
    │  PORT: CreateOrderUseCase (inbound)      │
    │  ┌────────────────────────────────────┐  │
    │  │  DOMAIN: Order, Money, OrderService │  │
    │  └────────────────────────────────────┘  │
    │  PORT: OrderRepository (outbound)         │
    └────┬────────────────────────────────────┘
         │
         └──────── Postgres adapter (secondary/driven)
```

| Concept | Meaning |
|---------|---------|
| **Port** | Interface the **application defines** — "I need to save orders" |
| **Adapter** | Infrastructure class that **implements** the port — Postgres, Kafka, Stripe |
| **Primary (driving)** | Outside world calls in — HTTP controller, CLI, message consumer |
| **Secondary (driven)** | App calls out — DB, email, payment gateway |
| **Dependency rule** | Adapters depend on ports; domain never depends on adapters |

**Clean Architecture rings (default):**

1. **Entities** — enterprise-wide business rules
2. **Use cases** — application-specific orchestration
3. **Interface adapters** — controllers, presenters, gateways
4. **Frameworks & drivers** — DB, web framework, external APIs

**Payoff:** Domain tests without containers; swap Postgres for in-memory; change REST to gRPC by new adapter only.

**Cost:** ~2–3× more types/files; overkill for CRUD with 5 tables and one developer.

---

## Microservices (distribution-level multi-tier)

Microservices are **not** a replacement for layers — each service is usually a **small layered or hexagonal app** deployed independently.

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

### Hexagonal package layout (Java/Kotlin/TS analogue)

```txt
domain/           # entities, domain services — zero infra imports
application/      # use cases + port interfaces (inbound/outbound)
adapters/
  in/web/         # REST controllers implement inbound ports
  out/persistence/# repositories implement outbound ports
```

### Scaling knobs per tier

| Tier | Scale lever | Watch |
|------|-------------|-------|
| Presentation | CDN, edge cache, static offload | Cache invalidation, auth on edge |
| Application | Horizontal pods, stateless design | Session stickiness, [[connection pooling]] |
| Data | Read replicas, sharding ([[database sharding]]) | Replica lag, cross-shard queries |
| Gateway | Rate limits ([[Token bucket]]), autoscale | Single point of misconfiguration |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Works in Postman, wrong in UI" | Client doing business logic (2-tier leak) | Move rules to [[Service Layer]]; UI displays only |
| Schema change breaks mobile app | Fat client queries DB or embeds SQL | API versioning; server-owned contract |
| Random data corruption | Handler writes DB without transaction | Wrap multi-table updates in service txn ([[ACID]]) |
| Can't unit test without Docker | Domain imports ORM/HTTP types | Introduce ports; in-memory adapters for tests |
| 15-hop sync chain, cascading timeouts | N-tier / microservice sprawl | Merge services or go async; [[backpressure]] |
| "Distributed monolith" — must deploy all 12 together | Shared DB, shared libs, circular calls | Database-per-service; define bounded contexts |
| Layer violation in PRs | Controller imports repository directly | Enforce module boundaries (archunit, eslint boundaries) |
| Gateway does business logic | BFF/gateway grew fat | Push rules to domain services; gateway routes/auth only |
| Performance fine in dev, slow in prod | Extra network tier not in local compose | Measure p99 per hop; colocate or cache |
| Team argues "3-tier vs microservices" | Conflating physical and logical | Draw two diagrams: deployment + module deps |

---

## Gotchas

> [!WARNING]
> **Tiers ≠ layers.** A team that "went to microservices" but kept one shared database and synchronous chains still has a **distributed monolith** — worst of both worlds.

> [!WARNING]
> **Skipping the service layer** — controllers that call repositories directly bypass validation, authz, and transactions. First shortcut becomes permanent.

> [!WARNING]
> **Anemic domain model** — entities are structs with getters; all logic in services. Works short-term; invariants scatter and duplicate across handlers.

> [!WARNING]
> **Hexagonal on a todo app** — ports/adapters for `TodoRepository`, `ClockPort`, `UuidPort` adds ceremony without boundary value. Use [[KISS]] until complexity earns structure.

> [!WARNING]
> **2-tier security illusion** — "only our app talks to the DB" — if the app ships DB credentials or RLS is weak, users own your data plane.

> [!WARNING]
> **Relaxed layering without documentation** — repository calls another service's HTTP API from the data layer. Debugging requires full stack traces across "layers."

> [!WARNING]
> **N-tier for resume-driven design** — API gateway + BFF + mesh + 6 services for 100 RPS. Operate what you draw; every box needs on-call.

---

## When NOT to use

| Pattern | Skip when |
|---------|-----------|
| **N-tier / microservices** | Team < 5, no independent scale profiles, no clear bounded contexts ([[KISS]]) |
| **Hexagonal / clean** | Short-lived CRUD, throwaway prototype, single developer |
| **2-tier (thick client)** | Rules must be centrally enforced; multiple client platforms |
| **Separate DAL tier** | Modern pools/ORM in app tier suffice; DAL-as-service adds latency |
| **Strict layering** | Hot path proven by profiling to need layer skip — document exception |

**Rule of thumb:** Default to **3-tier deployment + layered (or hexagonal) monolith**. Split tiers and services when you have **measured** pain: deploy frequency, scale shape, blast radius, or compliance boundary — not because the diagram looks enterprise.

---

## Related

**Layers in this vault:** [[presentation layer]] · [[Service Layer]] · [[frontend layered architecture]] · [[Database application]] · [[Orchestration layer]]

**Distribution & scale:** [[Microservice]] · [[distributed system]] · [[database sharding]] · [[stateless]] · [[event-driven]]

**Principles:** [[SOLID]] · [[KISS]] · [[DRY]] · [[Design pattern/Dependency Injection]]

**APIs between tiers:** [[gRPC]] · [[API design]] · [[HTTP module]]
