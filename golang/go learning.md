[[golang]] [[go]] [[go project]] [[Useful prompt for learning with AI chat]]

# go learning

> Go learning path — foundations → concurrency/HTTP → interview drills; use AI as a coach with tight feedback loops, not as a code vending machine.

---

## Mental model

**Say it in one breath:** Sequence beats random tutorials: syntax/types → interfaces/errors → goroutines/context → net/http + DB → tests/race → system-design talk tracks. After each exercise, force a review: idioms, errors, tests.

```txt
weeks 1–2  syntax, slices/maps, structs
weeks 3–4  methods, interfaces, errors
weeks 5–6  goroutines, channels, context
weeks 7–8  HTTP JSON middleware
weeks 9–10 SQL / sqlc or similar
weeks 11–12 tests, race, Docker
```

| Mode | Prompt shape |
|------|--------------|
| Concept drill | 60s explain + 3 examples + 5 Qs |
| Challenge | 50–100 lines + table tests |
| Review | Score 1–10 + idiomatic rewrite |

---

## Standard config / commands

```bash
# daily loop
go doc net/http.Server
go test ./... -race
go test -bench=. ./...
```

**Coach prompt skeleton:** teach `TOPIC` for Go backend interviews — differences from JS, 3 code samples, 5 questions one-by-one, wait for answers, score, then next exercise.

**Project prompt skeleton:** scaffold REST API (Gin/Echo + Postgres) with graceful shutdown, migrations, JWT — you implement handlers; AI reviews.

| Knob | Why it matters |
|------|----------------|
| 7–10h/week | Consistency > binge |
| Repo of solutions | Interview evidence |
| Race on concurrent work | Real Go skill |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Tutorial fog | No projects | Start [[go project]] #1 |
| Concurrency “magic” | Skipping channels | Build worker pool |
| Interview freeze | No timed mocks | 60m mock weekly |
| AI dependency | Pasting without review | Force line-by-line critique |
| JS habits in Go | Ignoring errors / classes | Re-read Effective Go |

---

## Gotchas

> [!WARNING]
> **AI greenfield dumps** — demand small diffs and tests you can run.

> [!WARNING]
> **Skipping `-race`** — false confidence on concurrent code.

> [!WARNING]
> **Frameworks first** — learn `net/http` before Gin magic.

---

## When NOT to use

- **Only watching videos** — type code.
- **LeetCode-only for Go jobs** — add HTTP + SQL projects.
- **Copying production secrets into prompts** — never.

---

## Related

[[go project]] [[go]] [[go-routines]] [[go interface]] [[Useful prompt for learning with AI chat]]
