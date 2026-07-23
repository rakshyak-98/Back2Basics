[[Python]] [[Docker compose]] [[Jenkins]]

# Airflow

> One-line: DAG scheduler for batch data/workflows — correctness = idempotent tasks + clear executor choice + SLA-aware ops — **Apache Airflow docs + on-call reality**.

## Mental model

Airflow defines **DAGs** (Directed Acyclic Graphs): tasks with dependencies, scheduled by interval or trigger. The **scheduler** parses DAGs, creates **DagRuns**, queues **TaskInstances**. **Workers** (executor-dependent) execute operators.

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
| Metadata DB | Source of truth for state — backup this |
| Executor | How tasks run: Sequential, Local, Celery, Kubernetes |
| Operator | Unit of work (`BashOperator`, `PythonOperator`, provider hooks) |
| Sensor | Waits for external condition (file, partition, flag) |

**Logical date (`execution_date`)** ≠ wall clock — it's the start of the data interval being processed. Backfill creates historical DagRuns.

## Standard config / commands

```shell
# CLI (inside scheduler/worker container or venv)
airflow dags list
airflow dags state my_dag 2025-07-22T00:00:00+00:00
airflow tasks list my_dag
airflow tasks test my_dag extract_task 2025-07-22   # dry run single task — no deps
airflow dags trigger my_dag --execution-date 2025-07-22T00:00:00+00:00
airflow tasks clear my_dag -s 2025-07-22 -e 2025-07-23 -y

# Logs
airflow tasks logs my_dag extract_task 2025-07-22T00:00:00+00:00 1
# or volume: /opt/airflow/logs/my_dag/extract_task/...

# DB health
airflow db check
```

### DAG skeleton (production patterns)

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-platform',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=1),
    'depends_on_past': False,          # True only when strict ordering required
}

with DAG(
    dag_id='daily_etl',
    default_args=default_args,
    schedule='0 2 * * *',              # cron — 02:00 UTC daily
    start_date=datetime(2025, 1, 1),
    catchup=False,                     # don't backfill on deploy unless intended
    max_active_runs=1,                 # prevent overlapping runs
    tags=['etl'],
) as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_fn)
    transform = PythonOperator(task_id='transform', python_callable=transform_fn)
    load = PythonOperator(task_id='load', python_callable=load_fn)
    extract >> transform >> load
```

### Executor choice

| Executor | When | Tradeoff |
|----------|------|----------|
| **Sequential** | Dev laptop only | One task at a time |
| **Local** | Small single-node | Parallel tasks, same machine |
| **Celery** | Mature multi-worker | Redis/Rabbit broker ops |
| **Kubernetes** | Isolated heavy tasks | Pod spin-up latency; best for spiky CPU |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| DAG missing from UI | Import errors in scheduler log | `airflow dags list-import-errors`; fix Python exception |
| Tasks stuck `scheduled` | Executor workers alive? Pool slots? | Scale workers; raise `pool` slots; clear zombie TIs |
| Tasks stuck `queued` | Celery/K8s queue depth | Worker connectivity; broker URL; K8s RBAC for pod launch |
| SLA miss emails | `sla=timedelta(hours=1)` on task | Optimize task; widen SLA if unrealistic; upstream data late |
| Sensor never completes | `poke` vs `reschedule`; timeout | Prefer `mode='reschedule'` to free worker; set `timeout` |
| Duplicate data loaded | Rerun without idempotency | Upsert keys; partition overwrite; `depends_on_past` review |
| Backfill storm | `catchup=True` on deploy | Set `catchup=False`; manual trigger with date range |
| DB connection errors | Metadata Postgres connections | PgBouncer; raise `sql_alchemy_pool_size`; recycle stale conns |
| Zombie tasks `running` after worker kill | Scheduler can't reach worker | `airflow tasks clear` failed TI; mark success/failed in UI carefully |
| Wrong data date processed | Confused logical vs run date | Use `{{ ds }}` / `data_interval_start` in Airflow 2.x templates |

### Sensor ops

```python
# Bad: occupies worker entire poke interval
FileSensor(filepath='/data/ready', poke_interval=60, timeout=3600)

# Better: release slot between pokes
FileSensor(filepath='/data/ready', mode='reschedule', poke_interval=300, timeout=3600)
```

## Gotchas

> [!WARNING]
> **Metadata DB loss = total orchestration amnesia.** Backup Postgres; treat restore drills seriously.

> [!WARNING]
> **`catchup=True` on first deploy** with years of `start_date` → thousands of DagRuns. Default `catchup=False`.

- **Top-level DAG code runs on every scheduler parse** — no heavy work at import; use factories sparingly.
- **`execution_date` templating changed in 2.x** — use `data_interval_start` / `logical_date` explicitly in new DAGs.
- **XCom default stores in metadata DB** — large payloads bloat DB; write to S3 and pass URI.
- **Pools** limit concurrency globally — `-1` slot starves unrelated DAGs if one pool misconfigured.
- **Local timezone in cron** — Airflow schedules UTC unless `default_timezone` set; DST surprises.

## When NOT to use

- Real-time streaming ETL → Kafka/Flink; Airflow is batch/interval orchestration.
- Simple cron on one server → systemd timer or K8s CronJob unless you need UI/dependencies.
- Long-running always-on services → deploy as service, not `BashOperator` loop.

## Related

[[Python]] · [[Docker compose]] · [[Jenkins]] · [[postgres]]
