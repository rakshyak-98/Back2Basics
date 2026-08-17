[[Architectures/Orchestration layer]] [[Airflow]] [[Jenkins]] [[Kubernates/kubectl]] [[Messaging/webhook]]

# Orchestration (DevOps)

> Central brain that sequences tasks and services into a workflow — retries, timeouts, and rollback live in one place (unlike choreography, where peers react to events).

```txt
        Orchestration (Dev ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask orchestration vs choreography to see if you pick a central w…

## Sources
- [Wikipedia — Orchestration (computing)](https://en.wikipedia.org/wiki/Orchestration_(computing)) — overview
- [Apache Airflow — DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) — deep-dive
- [[Architectures/Orchestration layer]] — deep-dive (distributed systems)

## Key Concepts
- **Central sequencing:** step B runs only after A succeeds → strict order and shared failure policy.
- **Retries / timeouts:** orchestrator owns recovery knobs → steps stay idempotent.
- **Compensating actions:** rollback or feature-flag off when a mid-pipeline step fails.
- **Choreography alternative:** services react to events
- **Decision signal:** 3+ dependent steps, or need for automated rollback → orchestrate


- **Core:** In DevOps, orchestration means a controller (pipeline engine, DAG scheduler, …

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

- Kubernetes Job / Helm pre-upgrade hook (light orchestration):

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

- Airflow-shaped DAG:

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

- Jenkins declarative stages:

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

## Mistakes to Avoid
- **Mistake:** DAGing a bash one-liner
- **Mistake:** Storing secrets in the DAG repository
- **Mistake:** Skipping idempotency — retries will double-charge or double-write
- **Mistake:** Running a non-HA scheduler for critical production workflows

## Pros/Cons or Trade-offs
- **Pro:** One place for retries, timeouts, visibility, and compensating actions.
- **Con:** Orchestrator becomes a single point of failure — HA the controller and metadata store.
- **Con:** Long synchronous pipelines block releases — split verify versus promote.

## Comparison
- vs choreography ([[Architectures/Orchestration layer]], [[Messaging/webhook]]): choreography scal…
- vs [[Jenkins]] pipelines: Jenkins is CI-oriented orchestration
- vs edge [[Edge orchestration tools for industrial IoT]]: same “desired workflow” idea, different …


### Use cases
- Release pipelines sequence test → migrate → deploy → smoke

- **Example:** Deploy succeeds but migration fails
