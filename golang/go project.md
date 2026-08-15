[[golang]] [[go learning]] [[go]] [[go-routines]] [[go cli]] [[gRPC]]

# go project

> Go practice projects — climb CLI → HTTP/SQL → concurrency → distributed; each has a clear scope and test bar.

## Interview Relevance

Project ladders show deliberate practice — interviewers care that you can scope CLI→HTTP→concurrency work with a clear test bar.

## Sources

- [Go project layout conventions (community)](https://github.com/golang-standards/project-layout) — overview
- [Go — Modules](https://go.dev/blog/using-go-modules) — overview

## Key Concepts

```txt
CLI → REST+DB → WS/gateway → KV/gRPC
```

| Level | Focus |
|-------|-------|
| Beginner | Structs, files, flags, tests |
| Intermediate | HTTP, SQL, auth, concurrency |
| Advanced | gRPC, multi-service, durability |

## Technical Details

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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Scope creep | Feature list grows | Cut to table above |
| Untestable main | Logic in `main` | Move to `internal` |
| Flaky concurrent tests | Timing asserts | Channels/`sync` + race |
| DB tests fragile | Shared DB | Testcontainers / tx rollback |
| “Done” without README | No decisions recorded | Write why section |

### Project ladder

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

**Production checklist (all):** structured logs, `-race` clean, health endpoint, configuration via environment, README with failure modes.

## Pros/Cons or Trade-offs

- **Trade-off:** Resume spam of 9 half-apps — ship 3 polished ones.
- **Trade-off:** Rewriting Kubernetes for learning — too wide.
- **Trade-off:** Copying entire starter kits — you won’t learn.

## Mistakes to Avoid

- Framework shopping — finish one stdlib HTTP service first.
- Skipping graceful shutdown — leaks in WS/chat projects.
- No idempotency on book/pay — instant production bug.
