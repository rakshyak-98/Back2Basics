[[Architectures/Orchestration layer]] [[DevOps/Airflow]] [[Kubernates/kubectl]] [[DevOps/Jenkins]]

# Orchestration (DevOps)

> Coordinate ordered steps, retries, and failure handling across services — central workflow vs scattered scripts — **CI/CD + runtime workflow engines**.

## Mental model

**Orchestration** sequences tasks/services to achieve a workflow. Contrast **choreography** (each service reacts to events without central brain) — see [[Architectures/Orchestration layer]] for distributed-systems detail.

```
Orchestrator (Airflow, Temporal, Jenkins pipeline)
    │
    ├─► Step A (deploy API) ──fail──► retry / rollback
    ├─► Step B (migrate DB) ──after A success
    └─► Step C (smoke test) ──notify on fail
```

Use orchestration when you need **central error handling**, **retries/timeouts**, **strict sequencing**.

## Standard config / commands

### When to orchestrate (decision table)

| Signal | Orchestrate? |
|--------|--------------|
| 3+ steps with dependencies | Yes |
| Compensating rollback on failure | Yes |
| Simple cron + one script | No — cron enough |
| Event-driven microservices only | Maybe choreography instead |

### Kubernetes job chain (light orchestration)

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
# Helm hook: pre-upgrade migrate before Deployment rollout
```

### Airflow DAG snippet

```python
from airflow.decorators import dag, task

@dag(schedule='@daily', catchup=False)
def etl():
    @task(retries=3, retry_delay=timedelta(minutes=5))
    def extract(): …

    @task
    def transform(): …

    extract() >> transform() >> load()
etl()
```

### Jenkins declarative pipeline

```groovy
pipeline {
  stages {
    stage('Test') { steps { sh 'npm test' } }
    stage('Deploy') {
      when { branch 'main' }
      steps { sh './deploy.sh' }
    }
  }
  post {
    failure { slackSend(color: 'danger', message: 'Deploy failed') }
  }
}
```

### Idempotency + timeouts

```bash
# Every orchestrated step should be safe to retry
curl -X POST --max-time 30 -H "Idempotency-Key: $BUILD_ID" …
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Pipeline stuck | Orchestrator worker down | Restart scheduler; clear zombie lock |
| Partial deploy | Step 3 failed after 1–2 succeeded | Automated rollback / feature flag off |
| Duplicate side effects | Retry without idempotency | Idempotency keys; mark completed steps |
| DAG never runs | `catchup=True` backlog | Disable catchup; reset start_date |
| K8s hook ran twice | Failed release retried | Helm hook weights + delete policy |

## Gotchas

> [!WARNING]
> **Orchestration becomes single point of failure** — HA the controller (Airflow metadata DB, Temporal cluster).

- **Refactoring hint:** avoid orchestration until workflow complexity justifies it — don't DAG a bash one-liner.
- **Secrets in DAG repo** — use vault/CI secrets, not plain text Variables.
- **Long synchronous pipelines** — block releases; split verify vs promote stages.

## When NOT to use

- Two independent cron jobs with no ordering — keep separate.
- High-scale event systems where central state doesn't scale — prefer choreography + [[Messaging/Web hooks]].

## Related

[[Architectures/Orchestration layer]] [[DevOps/Airflow]] [[Kubernates/kubectl]] [[DevOps/Jenkins]]
