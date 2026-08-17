[[golang]] [[go]] [[go project]] [[Useful prompt for learning with AI chat]] [[go-routines]] [[go interface]]

# go learning

> Go learning path — foundations → concurrency/HTTP → review drills; use AI as a coach with tight feedback loops, not as a code vending machine.

```txt
        go learning ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Learning-path notes signal how you ramp on Go for reviews

## Sources
- [A Tour of Go](https://go.dev/tour/) — overview
- [Go by Example](https://gobyexample.com/) — overview

## Key Concepts
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

## Technical Details
```bash
# daily loop
go doc net/http.Server
go test ./... -race
go test -bench=. ./...
```

- **Coach prompt skeleton:** teach `TOPIC` for Go backend depth checks

- **Project prompt skeleton:** scaffold REST API (Gin/Echo + Postgres) with gra…

| Knob | Why it matters |
|------|----------------|
| 7–10h/week | Consistency > binge |
| Repo of solutions | Review evidence |
| Race on concurrent work | Real Go skill |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Tutorial fog | No projects | Start [[go project]] #1 |
| Concurrency “magic” | Skipping channels | Build worker pool |
| Review freeze | No timed mocks | 60m mock weekly |
| AI dependency | Pasting without review | Force line-by-line critique |
| JS habits in Go | Ignoring errors / classes | Re-read Effective Go |

## Mistakes to Avoid
- **Mistake:** AI greenfield dumps — demand small diffs and tests you can run
- **Mistake:** Skipping `-race` — false confidence on concurrent code
- **Mistake:** Frameworks first — learn `net/http` before Gin magic

## Pros/Cons or Trade-offs
- **Trade-off:** Only watching videos — type code.
- **Trade-off:** LeetCode-only for Go jobs — add HTTP + SQL projects.
- **Trade-off:** Copying production secrets into prompts — never.
