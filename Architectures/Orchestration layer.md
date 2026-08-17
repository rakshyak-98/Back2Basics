[[Airflow]] [[Jenkins]] [[kafka]] [[webhook]] [[Idempotent-key]] [[ABR]]

# Orchestration layer

> Orchestration — a central coordinator drives the workflow; choreography — services react to events with no single brain.

```txt
        Orchestration laye ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Orchestration vs choreography is a system-design staple

## Sources
- [Microsoft — Choreography vs orchestration](https://learn.microsoft.com/en-us/azure/architecture/patterns/choreography) — overview
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/) — deep-dive

## Key Concepts
- **Note:** **Orchestration:** a central **coordinator** drives steps, knows global state…

```txt
Orchestration (Temporal/Airflow):
  Coordinator ──call──► Service A ──► Service B ──► Service C
       ▲                      │ fail → retry/compensate
       └──── state machine ──┘

Choreography (Kafka/events):
- **Note:** A publishes OrderCreated ──► B ships ──► B publishes Shipped ──► C bills
       (no single place shows full saga state)
```

| Style | Pros | Cons |
|-------|------|------|
| **Orchestration** | Visible workflow, retries, timeouts, debug | Coordinator availability; coupling to coordinator API |
| **Choreography** | Loose coupling, scale | Hard to trace; distributed debugging; implicit contract drift |

- **Note:** **Streaming note:** HLS/DASH manifests act as client-side [[Orchestration lay…

## Technical Details
### Tool placement

| Tool | Sweet spot | Not for |
|------|------------|---------|
| **Temporal** | Long-running sagas (days), human tasks, strong guarantees | Simple cron ETL |
| **Airflow** | Batch DAG/data pipelines, scheduled dependencies | Sub-second RPC chains |
| **Camunda / BPMN** | Human-in-loop approvals, regulated processes | High-throughput event streams |
| **AWS Step Functions** | AWS-native, serverless workflows | Complex local dev/test |
| **In-process state machine** | Single-service lifecycle | Cross-service compensation |
| **Kafka + outbox** | Event choreography backbone | Visual workflow without extra tooling |

### Temporal sketch (saga)

```typescript
export async function orderWorkflow(orderId: string) {
  await activities.reserveInventory(orderId);
  try {
    await activities.chargePayment(orderId);
    await activities.createShipment(orderId);
  } catch (e) {
    await activities.releaseInventory(orderId); // compensation
    throw e;
  }
}
// Worker polls task queue; history replay on failure — durable state
```

### Airflow sketch (batch)

```python
@dag(schedule='@daily')
def ingest():
    extract = BashOperator(task_id='extract', bash_command='...')
    transform = PythonOperator(task_id='transform', python_callable=...)
    load = PostgresOperator(task_id='load', ...)
    extract >> transform >> load
```

### When to orchestrate vs choreograph

```txt
Orchestrate when:
  - Multi-step saga with compensations
  - Human approval in the middle
  - Strict audit trail of each step
  - Timeouts per step (SLA)

Choreograph when:
  - Services already event-native ([[kafka]])
  - Flow rarely changes; teams own boundaries
  - Peak throughput > coordinator scale
  - Event schema versioning discipline exists
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Stuck workflow | Temporal UI / Airflow task logs | Retry policy; unblock signal; kill zombie run |
| Double charge / ship | Idempotency keys missing | [[Idempotent-key]] on activities; dedupe table |
| Lost saga state | Choreography-only — no central view | Add correlation ID logging; consider orchestrator |
| Airflow backlog | Scheduler health; pool slots | Scale workers; reduce concurrency cap |
| Version skew | Worker deploy mid-workflow | Temporal workflow versioning; compatible activity changes |
| "Works in dev" timeout | Step Functions 25s lambda limit | Break steps; use activity workers |

## Mistakes to Avoid
- **Mistake:** Orchestrator as SPOF
- **Mistake:** Choreography saga without compensating events
- **Mistake:** Airflow for online traffic
- **Mistake:** BPMN for engineers who hate XML
- **Mistake:** Nested orchestrators

## Pros/Cons or Trade-offs
- **Trade-off:** Single CRUD service — domain logic in application code suffices.
- **Trade-off:** Sync request/response chain < 3 hops — direct calls + [[Idempotent-key]].
- **Trade-off:** **Replace [[kafka]]** with Airflow — different problems; often complement (Airflow consumes Kafka).
