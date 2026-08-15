[[golang]] [[go]] [[go project]] [[Useful prompt for learning with AI chat]] [[go-routines]] [[go interface]]

# go learning

> Go learning path — foundations → concurrency/HTTP → interview drills; use AI as a coach with tight feedback loops, not as a code vending machine.

## Interview Relevance

Learning-path notes signal how you ramp on Go for interviews — foundations, concurrency, then drills — without treating AI as a code vending machine.

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

**Coach prompt skeleton:** teach `TOPIC` for Go backend interviews — differences from JS, 3 code samples, 5 questions one-by-one, wait for answers, score, then next exercise.

**Project prompt skeleton:** scaffold REST API (Gin/Echo + Postgres) with graceful shutdown, migrations, JWT — you implement handlers; AI reviews.

| Knob | Why it matters |
|------|----------------|
| 7–10h/week | Consistency > binge |
| Repo of solutions | Interview evidence |
| Race on concurrent work | Real Go skill |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Tutorial fog | No projects | Start [[go project]] #1 |
| Concurrency “magic” | Skipping channels | Build worker pool |
| Interview freeze | No timed mocks | 60m mock weekly |
| AI dependency | Pasting without review | Force line-by-line critique |
| JS habits in Go | Ignoring errors / classes | Re-read Effective Go |

## Pros/Cons or Trade-offs

- **Trade-off:** Only watching videos — type code.
- **Trade-off:** LeetCode-only for Go jobs — add HTTP + SQL projects.
- **Trade-off:** Copying production secrets into prompts — never.

## Mistakes to Avoid

- AI greenfield dumps — demand small diffs and tests you can run.
- Skipping `-race` — false confidence on concurrent code.
- Frameworks first — learn `net/http` before Gin magic.
