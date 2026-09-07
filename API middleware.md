The architecture pressure appears when **cross-cutting concerns** become numerous enough that endpoint code dominated by infrastructure logic rather than business behavior.

> [!WARNING]
> Centralize cross-cutting concerns in middleware when policies span multiple endpoints, the cost in pipeline overhead and centralized ordering complexity.

**Middleware exists because repeated infrastructure concerns must be enforced independently of endpoint business logic.**

- Shared functions reduce duplication, middleware controls when shared logic executes.
Whenever a request can be rejected using information already available at the middleware boundary -- for example, missing credentials, invalid authentication, exceeded rate limits, or malformed request metadata.
**Middleware short-circuiting** terminates the pipeline at the cheapest point where the policy can be evaluated.

> [!WARNING]
> Early rejection requires middleware to have enough **context** to make the decision, which can increase coupling between middleware and request metadata. It stops being appropriate when determining validity requires business domain state that only the handler or domain service legitimately owns.

> Middleware works because each layer receives the request context and a mechanism such as `next()` that transfer control to the next layer.

The important mechanism is **short-circuiting** a middleware can either invoke the next stage or return a response immediately. 

**Choosing middleware validation means validation rules must be separated from domain invariants that require business logic.**

**Explicit pipeline ordering** make dependencies deterministic and allows expensive work to be avoided after an earlier rejection.

> [!WARNING]
> Ordering becomes part of the system's correctness model. Adding or moving middleware can therefore change security, latency, and observability behavior even when the individual middleware implementation has not changed.

**Order middleware explicitly when stages have dependencies or resource protection priorities**. The cost is that pipeline order becomes a correctness constraint.

## Keep middleware Infrastructure-Oriented, Not Business-Logic Oriented
The decision becomes important when engineers start adding domain-specific branching to middleware for example, middleware containing different pricing, order, payment, or customer-state rules for different endpoints. There is **no clean numerical threshold**. The trigger is business logic becoming dependent on route specific semantics.

> [!NOTE]
> At the **boundary between the API infrastructure layer and application/domain layer**, middleware should establish request context and enforce transport-level policies; domain services should decide business outcomes.

**Business logic in middleware** creates hidden dependencies because behavior occurs before the handler and may very based on routing details.
**Handler/domain implementation** keeps domain decisions close to the data and invariants they govern.
Keeping middleware infrastructure-oriented preserves the pipeline as a reusable enforcement layer.

> "Some policies that look like middleware concerns must remain in application code, even if centralizing them would appear more convenient. This creates some duplication when domain rules genuinely differ between endpoints, but prevents the middleware layer from becoming a second business-logic runtime."

- Choosing infrastructure-only middleware means domain authorization rules may require explicit service-layer checks.
- Handlers cannot assume middleware has enforced business invariants unless that policy is explicitly defined as middleware responsibility.
- Middleware must remain usable across endpoints without understanding their internal domain models.

## Centralize Error and Observability handling around the pipeline 
**Handle common API errors and request observability centrally in middleware** rather than implementing them independently in every handler.
When multiple endpoints must produce consistent error responses or telemetry fields such as request IDs, status codes, latency, and structured logs. There is **no fixed traffic threshold**; The trigger is consistency becoming operationally important across the API surface.

Around the **request/response pipeline**, so middleware can observe both downstream execution and the resulting response/error. It must sit around the handler rather then only before it because failures and latency often become visible only after downstream processing begins.

**Per-handler logging/error formatting** produces inconsistenc

## Trade-off as Consequences

**Latency** Each middleware adds processing work, so a long chain increases per-request latency.
**Execution complexity** Middleware ordering become significant because authentication, authorization, validation and rate limiting can depend on one another. The abstraction become harmful when the chain is so large that engineers cannot determine which layer modifies or terminates a request.
**Debuggability** Control moves away from the handler into distributed pipeline stages, making failures harder to trace. This cost dominates when middleware performs substantial business logic rather than narrow cross-cutting work.
**Flexibility** Global middleware applies broadly, so endpoint-specific exceptions require explicit routing or configuration. The trade stops begin worthwhile when a supposedly shared policy has more exception than common behavior.

"The abstraction also makes migration harder because moving a policy out of middleware requires identifying every route that implicitly depends on its behavior. As the chain grows, teams are forced toward explicit ordering rules, middleware ownership, observability, and separation between **infrastructure middleware**" and business specific logic.