[[Architectures/Orchestration layer]] [[Airflow]] [[Jenkins]] [[Kubernates/kubectl]] [[Messaging/webhook]]

# Orchestration (DevOps)

> Central brain that sequences tasks and services into a workflow — retries, timeouts, and rollback live in one place (unlike choreography, where peers react to events).





## Interview Relevance
Interviewers ask orchestration vs choreography to see if you pick a central workflow engine when order, compensation, and failure policy matter — and avoid DAGing a one-line cron.

## Sources
- [Wikipedia — Orchestration (computing)](https://en.wikipedia.org/wiki/Orchestration_(computing)) — overview
- [Apache Airflow — DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) — deep-dive
- [[Architectures/Orchestration layer]] — deep-dive (distributed systems)

## Core Definition
In DevOps, orchestration means a controller (pipeline engine, DAG scheduler, or workflow system) drives multi-step work with explicit dependencies, retries, and central error handling — contrast event-driven choreography without a single director.

## Key Concepts
- **Central sequencing:** step B runs only after A succeeds → strict order and shared failure policy.
- **Retries / timeouts:** orchestrator owns recovery knobs → steps stay idempotent.
- **Compensating actions:** rollback or feature-flag off when a mid-pipeline step fails.
- **Choreography alternative:** services react to events — better at high scale when central state does not fit.
- **Decision signal:** 3+ dependent steps, or need for automated rollback → orchestrate; simple cron → do not.

## Technical Details
```
Orchestrator (Airflow, Temporal, Jenkins pipeline)
    │
    ├─► Step A (deploy API) ──fail──► retry / rollback
    ├─► Step B (migrate DB) ──after A success
    └─► Step C (smoke test) ──notify on fail
```

| Signal | Orchestrate? |
|--------|--------------|
| 3+ steps with dependencies | Yes |
| Compensating rollback on failure | Yes |
| Simple cron + one script | No — cron enough |
| Event-driven microservices only | Maybe choreography instead |

Kubernetes Job / Helm pre-upgrade hook (light orchestration):

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: migrate
spec:
  template:
    spec:
      restartPolicy: OnFailure
      containers:
        - name: migrate
          image: myapp:migrate
```

Airflow-shaped DAG:

```python
from airflow.decorators import dag, task

@dag(schedule='@daily', catchup=False)
def etl():
    @task(retries=3)
    def extract(): ...

    @task
    def transform(): ...

    extract() >> transform()
etl()
```

Jenkins declarative stages:

```groovy
pipeline {
  stages {
    stage('Test') { steps { sh 'npm test' } }
    stage('Deploy') {
      when { branch 'main' }
      steps { sh './deploy.sh' }
    }
  }
}
```

```bash
# Every orchestrated step should be safe to retry
curl -X POST --max-time 30 -H "Idempotency-Key: $BUILD_ID" …
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Pipeline stuck | Worker / scheduler down | Restart; clear zombie lock |
| Partial deploy | Mid-step failure | Automated rollback / flag off |
| Duplicate side effects | Retry without idempotency | Idempotency keys; mark completed steps |
| DAG never runs | Catchup backlog | Disable catchup; reset start date |
| Helm hook ran twice | Failed release retried | Hook weights + delete policy |

## Real-World Applications
Release pipelines sequence test → migrate → deploy → smoke; data platforms use [[Airflow]] DAGs for extract/transform/load with retries.

**Example:** Deploy succeeds but migration fails — without orchestration you leave a half-applied release; with it you roll back or stop promotion.

## Pros/Cons or Trade-offs
- **Pro:** One place for retries, timeouts, visibility, and compensating actions.
- **Con:** Orchestrator becomes a single point of failure — HA the controller and metadata store.
- **Con:** Long synchronous pipelines block releases — split verify versus promote.

## Comparison
- vs choreography ([[Architectures/Orchestration layer]], [[Messaging/webhook]]): choreography scales event peers; orchestration owns strict sequence and compensation.
- vs [[Jenkins]] pipelines: Jenkins is CI-oriented orchestration; [[Airflow]] is batch/data DAG orchestration.
- vs edge [[Edge orchestration tools for industrial IoT]]: same “desired workflow” idea, different constraints (offline, OT).

## Mistakes to Avoid
- DAGing a bash one-liner — wait until workflow complexity justifies a controller.
- Storing secrets in the DAG repository — use a vault or CI secret store.
- Skipping idempotency — retries will double-charge or double-write.
- Running a non-HA scheduler for critical production workflows.
