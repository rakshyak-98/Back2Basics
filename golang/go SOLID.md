[[golang/go embedding]] [[golang/go build]] [[Design pattern/Static Members]]

# Go SOLID (idiomatic Go)

> SOLID adapted to Go's interfaces, composition, and small-package culture — not Java inheritance.

## Mental model

Go favors **composition over inheritance**. Interfaces are implicit (duck typing). SOLID still applies but looks different: small interfaces (ISP), struct embedding (OCP-ish), constructor functions (DIP via interfaces in main).

| Principle | Go expression |
|-----------|---------------|
| **S** Single responsibility | One package/type, one reason to change |
| **O** Open/closed | Embed interfaces; extend via new types |
| **L** Liskov | Implement interface without surprising callers |
| **I** Interface segregation | `io.Reader`, `io.Writer` — tiny interfaces |
| **D** Dependency inversion | Depend on interfaces; wire in `main` |

## Standard config / commands

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

## Triage (when things break)

| Smell | Check | Fix |
|-------|-------|-----|
| God struct with 20 methods | Package size | Split by domain; extract interfaces |
| Interface with 15 methods | Call sites | Split into Reader/Writer-style interfaces |
| Concrete type in constructor everywhere | Tests hard | Accept interface in `New*` |
| Embedding leaks methods | Promoted methods | Embed unexported helper struct |
| `interface{}` everywhere | Type assertions | Generics or specific interfaces |

## Gotchas

> [!WARNING]
> **Interfaces only declare methods** — no fields on interfaces in Go.
>
> **Premature interfaces** — define at consumer, not producer ("accept interfaces, return structs").
>
> **Embedding for "inheritance"** — promoted methods can break LSP if base type isn't substitutable.

## When NOT to use

- Don't create `IService`, `IRepository` for every type — Go idiom is minimal interfaces at boundaries.
- Don't force Java-style abstract factories when a function literal suffices.

## Related

[[golang/go embedding]] [[golang/go build]] [[Design pattern/method shadowing]]
