[[Airflow]] [[Jenkins]] [[kafka]] [[webhook]] [[Idempotent-key]]

# Orchestration layer

> Workflow **orchestration** vs **choreography** — where Temporal, Airflow, Camunda, and step functions sit — **distributed systems design**.

---

## Mental model

**Orchestration:** a central **coordinator** drives steps, knows global state, retries, timeouts, compensations. **Choreography:** each service reacts to **events** with no central brain — flow emerges from message contracts.

```txt
Orchestration (Temporal/Airflow):
  Coordinator ──call──► Service A ──► Service B ──► Service C
       ▲                      │ fail → retry/compensate
       └──── state machine ──┘

Choreography (Kafka/events):
  A publishes OrderCreated ──► B ships ──► B publishes Shipped ──► C bills
       (no single place shows full saga state)
```

| Style | Pros | Cons |
|-------|------|------|
| **Orchestration** | Visible workflow, retries, timeouts, debug | Coordinator availability; coupling to coordinator API |
| **Choreography** | Loose coupling, scale | Hard to trace; distributed debugging; implicit contract drift |

**Streaming note:** HLS/DASH manifests act as client-side [[Orchestration layer]] for rendition selection — different domain, same word.

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stuck workflow | Temporal UI / Airflow task logs | Retry policy; unblock signal; kill zombie run |
| Double charge / ship | Idempotency keys missing | [[Idempotent-key]] on activities; dedupe table |
| Lost saga state | Choreography-only — no central view | Add correlation ID logging; consider orchestrator |
| Airflow backlog | Scheduler health; pool slots | Scale workers; reduce concurrency cap |
| Version skew | Worker deploy mid-workflow | Temporal workflow versioning; compatible activity changes |
| "Works in dev" timeout | Step Functions 25s lambda limit | Break steps; use activity workers |

---

## Gotchas

> [!WARNING]
> **Orchestrator as SPOF** — HA cluster + persistence (Temporal/Camunda DB) required for prod.

> [!WARNING]
> **Choreography saga without compensating events** — partial failure leaves inconsistent state.

> [!WARNING]
> **Airflow for online traffic** — wrong latency model; batch scheduler not RPC bus.

> [!WARNING]
> **BPMN for engineers who hate XML** — adoption dies; pick code-first (Temporal) if team is dev-heavy.

> [!WARNING]
> **Nested orchestrators** — Airflow triggers Step Functions triggers Lambda — observability nightmare; one primary layer.

---

## When NOT to use

- **Single CRUD service** — domain logic in app code suffices.
- **Sync request/response chain < 3 hops** — direct calls + [[Idempotent-key]].
- **Replace [[kafka]]** with Airflow — different problems; often complement (Airflow consumes Kafka).

---

## Related

[[Airflow]] [[Jenkins]] [[kafka]] [[webhook]] [[Idempotent-key]] [[ABR]]
