[[golang/go embedding]] [[golang/go build]] [[Design pattern/Static Members]] [[Design pattern/method shadowing]]

# Go SOLID (idiomatic Go)

> SOLID adapted to Go's interfaces, composition, and small-package culture — not Java inheritance.

```txt
        Go SOLID (idiomati ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** SOLID in Go interviews tests whether you map SRP/ISP/DIP onto small interface…

## Sources
- [Go blog — Go Proverbs](https://go-proverbs.github.io/) — overview
- [Effective Go](https://go.dev/doc/effective_go) — deep-dive
- [Wikipedia — SOLID](https://en.wikipedia.org/wiki/SOLID) — overview

## Key Concepts
| Principle | Go expression |
|-----------|---------------|
| **S** Single responsibility | One package/type, one reason to change |
| **O** Open/closed | Embed interfaces; extend via new types |
| **L** Liskov | Implement interface without surprising callers |
| **I** Interface segregation | `io.Reader`, `io.Writer` — tiny interfaces |
| **D** Dependency inversion | Depend on interfaces; wire in `main` |

## Technical Details
### Interface segregation (accept interfaces, return structs)

```go
type Logger interface {
    Info(msg string, args ...any)
}

type Service struct {
    log Logger
}

func NewService(log Logger) *Service {
    return &Service{log: log}
}
```

### Composition over inheritance

```go
type Animal interface {
    Speak() string
}

type Dog struct{}

func (Dog) Speak() string { return "Woof" }

func MakeSpeak(a Animal) {
    fmt.Println(a.Speak())
}
```

### DIP — wire dependencies in main

```go
func main() {
    log := slog.Default()
    svc := NewService(log)
    svc.Run()
}
```

### Testing with fakes

```go
type fakeLogger struct{}

func (fakeLogger) Info(string, ...any) {}
```

### Failure signals

| Smell | Check | Fix |
|-------|-------|-----|
| God struct with 20 methods | Package size | Split by domain; extract interfaces |
| Interface with 15 methods | Call sites | Split into Reader/Writer-style interfaces |
| Concrete type in constructor everywhere | Tests hard | Accept interface in `New*` |
| Embedding leaks methods | Promoted methods | Embed unexported helper struct |
| `interface{}` everywhere | Type assertions | Generics or specific interfaces |

## Mistakes to Avoid
- **Mistake:** Interfaces only declare methods

## Pros/Cons or Trade-offs
- **Trade-off:** Don't create `IService`, `IRepository` for every type — Go idiom is minimal interfaces at boundaries.
- **Trade-off:** Don't force Java-style abstract factories when a function literal suffices.
