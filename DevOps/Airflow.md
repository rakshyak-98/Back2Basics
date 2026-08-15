[[orchestration]] [[Jenkins]] [[Python]] [[Docker compose]] [[postgres]] [[Slack]]

# Airflow

> Apache Airflow schedules batch workflows as DAGs (Directed Acyclic Graphs) — tasks with dependencies, retries, and a metadata database as the source of truth.

## Interview Relevance

Interviewers ask Airflow to check whether you know scheduler vs workers vs metadata DB, logical date vs wall clock, `catchup` storms, and when batch DAGs beat streaming or a simple cron.

## Sources

- [Apache Airflow — DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) — deep-dive
- [Apache Airflow — Executors](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html) — deep-dive
- [Wikipedia — Apache Airflow](https://en.wikipedia.org/wiki/Apache_Airflow) — overview

## Core Definition

Airflow is a workflow platform: you define DAGs in Python; the scheduler creates DagRuns and TaskInstances; an executor (Local, Celery, Kubernetes, …) runs operators on workers; state lives in a metadata database (usually PostgreSQL).

## Key Concepts

- **DAG:** directed acyclic graph of tasks and dependencies → the workflow shape.
- **Scheduler:** parses DAGs, enqueues ready tasks when upstream succeeds.
- **Metadata DB:** source of truth for DagRun/TaskInstance state — back it up.
- **Executor:** how work runs (Sequential, Local, Celery, Kubernetes) → ops trade-offs.
- **Operator / Sensor:** unit of work vs wait-for-external-condition.
- **Logical date / data interval:** identifies the data period being processed — not “when the task started.”

## Technical Details

```
Scheduler ──► DagRun (logical date) ──► TaskInstance queue ──► Worker
     ▲                              │
     └── metadata DB (Postgres) ◄───┘ state transitions
Webserver UI ── reads same DB
```

| Component | Role |
|-----------|------|
| Scheduler | Enqueues tasks when dependencies met |
| Webserver | UI + API |
| Metadata DB | Source of truth for state |
| Executor | Sequential / Local / Celery / Kubernetes |
| Operator | Unit of work (`BashOperator`, `PythonOperator`, …) |
| Sensor | Waits for file, partition, flag, etc. |

```shell
airflow dags list
airflow dags state my_dag 2025-07-22T00:00:00+00:00
airflow tasks test my_dag extract_task 2025-07-22
airflow dags trigger my_dag --execution-date 2025-07-22T00:00:00+00:00
airflow tasks clear my_dag -s 2025-07-22 -e 2025-07-23 -y
airflow db check
```

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-platform',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=1),
    'depends_on_past': False,
}

with DAG(
    dag_id='daily_etl',
    default_args=default_args,
    schedule='0 2 * * *',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['etl'],
) as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_fn)
    transform = PythonOperator(task_id='transform', python_callable=transform_fn)
    load = PythonOperator(task_id='load', python_callable=load_fn)
    extract >> transform >> load
```

| Executor | When | Tradeoff |
|----------|------|----------|
| **Sequential** | Laptop only | One task at a time |
| **Local** | Small single-node | Parallel on one machine |
| **Celery** | Multi-worker fleet | Redis/RabbitMQ broker ops |
| **Kubernetes** | Isolated heavy tasks | Pod start latency; good for spiky CPU |

Prefer `mode='reschedule'` on sensors so they release worker slots between pokes.

| Symptom | Check | Fix |
|---------|-------|-----|
| DAG missing from UI | Import errors in scheduler log | `airflow dags list-import-errors` |
| Tasks stuck `scheduled` | Workers / pool slots | Scale workers; raise pool slots |
| Tasks stuck `queued` | Broker / K8s RBAC | Fix connectivity; pod launch rights |
| Duplicate data loaded | Rerun without idempotency | Upsert; partition overwrite |
| Backfill storm | `catchup=True` + old `start_date` | Default `catchup=False` |
| Zombie `running` tasks | Worker died | Clear TaskInstance carefully |

## Real-World Applications

Nightly ETL: extract from warehouse APIs, transform, load partitions; sensors wait for upstream files then kick off loads.

**Example:** First deploy with years of `start_date` and `catchup=True` queues thousands of DagRuns — set `catchup=False` and backfill deliberately.

## Pros/Cons or Trade-offs

- **Pro:** Rich UI, dependency graph, retries, and Python-native DAGs for batch pipelines.
- **Con:** Metadata DB loss means orchestration amnesia — treat Postgres restore as critical.
- **Con:** Not a streaming engine — Kafka/Flink for real-time; not a long-running service host.

## Comparison

- vs cron / Kubernetes CronJob: Airflow wins when you need UI, dependencies, and retries across many tasks.
- vs [[Jenkins]]: Jenkins is CI/CD; Airflow is data/batch workflow scheduling.
- vs [[orchestration]] generally: Airflow is one concrete orchestrator optimized for scheduled DAGs.

## Mistakes to Avoid

- Heavy work at DAG import time — top-level code runs on every scheduler parse.
- Stuffing large XCom payloads in the metadata DB — write to object storage and pass URIs.
- Occupying workers with long `poke` sensors — use `reschedule` mode and timeouts.
- Confusing logical date with wall-clock run time in templates.
- Using Airflow to run always-on services inside a `BashOperator` loop.
