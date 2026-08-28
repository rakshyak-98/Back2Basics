The exact number of layers is not important. **N-tier** simply means separating the system into multiple tiers based on responsibility. **What responsibility belongs where, and why?**

"A Layer should exist because it provides a **boundary**" HTTP changes, Business Logic, Database changes, Domain logic.

```txt
        Things that change frequently
                    ↓
    ┌───────────────────────────┐
    │ HTTP / API                │
    ├───────────────────────────┤
    │ Application Use Cases     │
    ├───────────────────────────┤
    │ Domain / Business Rules   │
    ├───────────────────────────┤
    │ Infrastructure            │
    │ DB / Cache / External API │
    └───────────────────────────┘
                    ↑
        Things implementation-specific
```

"If this part changes, how much of the rest of my application needs to change?"

```txt
Restaurant Owner
      ↓
POST /promotions
      ↓
Validate request
      ↓
Check restaurant subscription
      ↓
Create promotion
      ↓
Generate video using external AI provider
      ↓
Store video
      ↓
Return promotion status
```
- Should all of this logic exist inside the API controller?

## Presentation Layer (Request receiver)

**"Does this code deal with transport?"** HTTP, JSON, gRPC, WebSocket

The layer that receives request from the outside world.

its responsibility is primarily:
```txt
HTTP Request
     ↓
Parse JSON
     ↓
Validate basic request format
     ↓
Call application logic
     ↓
Convert result to HTTP response
```

```go
func CreatePromotion(w http.ResponseWriter, r *http.Request) {
    var req CreatePromotionRequest

    json.NewDecoder(r.Body).Decode(&req)

    promotion, err := promotionService.Create(req)

    // Convert result/error into HTTP response
}
```
The controller should not know: Should translate HTTP to Application
- How a promotion is stored
- How the video provider works internally
- How subscription billing works
- Database queries

## Application/Service Layer (Orchestration)

**"Does this code coordinate a user/system action?"** Create promotion, Publish promotion, Generate video, Cancel subscription

This is where the **use case orchestration** happens.

The service decides the sequence:
```txt
1. Find restaurant
2. Check permissions
3. Check subscription
4. Create promotion record
5. Trigger video generation
6. Return result
```

Application layer often the **orchestrator of a use case**. Import the service needed to do resolve the request and control the sequence of the resolve.
**The Application layer does not necessarily import "Services" only.** It can coordinate repositories, domain objects, external gateways, event publishers, and other abstraction.

> [!INFO]
> It receives a use-case request and coordinates the required collaborators to move the system from its current state to the desired outcome.

```go
func (s *PromotionService) CreatePromotion(...) error {

    restaurant := s.restaurantRepo.Get(...)

    s.subscriptionService.Validate(restaurant)

    promotion := NewPromotion(...)

    s.promotionRepo.Save(promotion)

    s.videoService.Generate(promotion)

    return nil
}
```

> [!INFO]
> The application layer orchestrates a use case. It coordinates the services and dependencies needed to fulfill a request and controls the sequence in which the work happens. [[Application Layer]]
> 1. Get restaurant
> 2. Check subscription
> 3. Create promotion
> 4. Save promotion
> 5. Trigger video generation
> 6. Return the result

## Domain/Business Layer (Rules)

**"Does this code define a business rule?"** Promotion cannot be published before generation completes

The rules define in Business Layer should ideally not depend on

```txt
HTTP
Database
Redis
AWS
Stripe
External APIs
```
- instead of directly updates on the data, it enforce a rule to update the data. So the related data update rules remains in one place. [[Domain Layer]]

## Data Access Layer (Data retrieve/persist)

Defines how the application access the format of data. It holds the Data Interfaces. [[Data access Layer]]
```go
type PromotionRepository interface {
    Save(promotion *Promotion) error
    FindByID(id string) (*Promotion, error)
}
```

> [!NOTE]
> The Domain and Application Layer should not control or depend on the implementation. It should depend on the interface. So if tomorrow Database connector is changed, without changing the business logic.

> [!NOTE]
> The service does not need to know whether the implementation uses: MongoDB, DynamoDB, PostgreSQL, Service Layer just call `promotionRepo.Save(pormotion)`

## Infrastructure Layer (Implementations communication to external)

**"Does this code talk to an external system?"** Database, Redis, S3, Video AI provider, Stripe, Kafka

```go
type VideoGenerator interface {
    Generate(prompt string) (Video, error)
}
```
- Because of the interface **the application logic depend `VideoGenerator` not directly on `EvatorVideoGenerator`**

[[Infrastructure Layer]] Infrastructure should generally hold the implementation, not the interface. The application and domain side owns the abstraction deciding what it needs. **Infrastructure provides the concrete implementation**. [[h]]