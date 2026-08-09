[[golang]] [[go learning]] [[go]] [[go-routines]]

# go project

> Go practice projects — climb CLI → HTTP/SQL → concurrency → distributed; each has a clear scope and test bar.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Project ladder]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** One project at a time with README “why”, table-driven tests, and graceful shutdown. Prefer boring stdlib until the project forces a library.

```txt
CLI → REST+DB → WS/gateway → KV/gRPC
```

| Level | Focus |
|-------|-------|
| Beginner | Structs, files, flags, tests |
| Intermediate | HTTP, SQL, auth, concurrency |
| Advanced | gRPC, multi-service, durability |

---

## Standard config / commands

```bash
go mod init github.com/you/proj
mkdir -p cmd/app internal
go test ./... -race
docker compose up -d # when Postgres required
```

| Knob | Why it matters |
|------|----------------|
| `internal/` | Keep API surface small |
| Context on servers | Cancel on SIGINT |
| Idempotent writes | Booking/payment style tasks |

---

## Project ladder

| # | Project | Must include |
|---|---------|--------------|
| 1 | CLI todo | JSON persist, flags, table output, unit tests |
| 2 | URL shortener CLI | base62, LRU, benchmarks |
| 3 | File stats | Concurrent walk, SIGINT shutdown, JSON/CSV |
| 4 | REST tasks API | CRUD filters, JWT, Postgres, integration tests |
| 5 | Chat server | Rooms, broadcast, rate limit |
| 6 | API gateway | Auth + rate limit + proxy |
| 7 | KV store | gRPC, replication or Raft-lite |
| 8 | Booking service | Idempotent book, services split |
| 9 | Log aggregator | Ingest + query + backpressure |

**Production checklist (all):** structured logs, `-race` clean, health endpoint, config via env, README with failure modes.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Scope creep | Feature list grows | Cut to table above |
| Untestable main | Logic in `main` | Move to `internal` |
| Flaky concurrent tests | Timing asserts | Channels/`sync` + race |
| DB tests fragile | Shared DB | Testcontainers / tx rollback |
| “Done” without README | No decisions recorded | Write why section |

---

## Gotchas

> [!WARNING]
> **Framework shopping** — finish one stdlib HTTP service first.

> [!WARNING]
> **Skipping graceful shutdown** — leaks in WS/chat projects.

> [!WARNING]
> **No idempotency on book/pay** — instant production bug.

---

## When NOT to use

- **Resume spam of 9 half-apps** — ship 3 polished ones.
- **Rewriting Kubernetes for learning** — too wide.
- **Copying entire starter kits** — you won’t learn.

---

## Related

[[go learning]] [[go cli]] [[go-routines]] [[gRPC]]
