[[golang]] [[Design pattern]] [[java]] [[method shadowing]]

# Go embedding (struct and interface)

> Anonymous field embedding — promotes methods and fields for convenient delegation; **not** classical inheritance; conflicts resolve by explicit outer rules.

```txt
        Go embedding (stru ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Embedding vs inheritance is a frequent Go design question

## Sources
- [Effective Go — Embedding](https://go.dev/doc/effective_go#embedding) — deep-dive
- [Go spec — Struct types](https://go.dev/ref/spec#Struct_types) — deep-dive

## Key Concepts
```go
type Reader struct { io.Reader }  // embed interface
type Engine struct { hp int }
type Car struct {
- **Note:** Engine // promoted: Car.hp, Car methods if any on Engine
    brand string
}
```

Two cases:
- **Note:** 1. **Embed struct**
- **Note:** 2. **Embed interface**

- **Note:** No virtual dispatch chain

## Technical Details
### Struct embedding — promotion

```go
type Logger struct{}

func (Logger) Log(msg string) { fmt.Println(msg) }

type Server struct {
    Logger // anonymous embed
    addr string
}

s := Server{}
s.Log("starting") // promoted — equivalent to s.Logger.Log
```

### Override outer method

```go
func (s Server) Log(msg string) {
    fmt.Printf("[%s] %s\n", s.addr, msg)
}
// s.Log calls Server.Log, not Logger.Log
```

### Interface embedding — compose interfaces

```go
type ReadWriter interface {
    io.Reader
    io.Writer
}
// ReadWriter requires both method sets
```

### Embed interface for forward-compatible wrapper

```go
type HTTPClient struct {
    http.Client // embed concrete struct
}

func (c *HTTPClient) Do(req *http.Request) (*http.Response, error) {
    // override Do, fall back to embedded for other methods
    return c.Client.Do(req)
}
```

### Explicit field when names collide

```go
type A struct{ X int }
type B struct{ X int }
type C struct {
    A
    B // C.X is ambiguous — must use C.A.X or C.B.X
}
```

### Constructor pattern

```go
func NewServer(addr string) *Server {
    return &Server{
        Logger: Logger{},
        addr:   addr,
    }
}
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `ambiguous selector X` | Two embeds expose same field/method | Qualify `outer.A.X`; rename or drop embed |
| Interface not satisfied | Embedded interface nil | Initialize embedded field; implement missing methods on outer |
| Method not promoted | Unexported (lowercase) method | Export method or wrap with exported forwarder |
| Unexpected nil panic | Embedded pointer nil | Use value embed or construct with `&T{}` |
| JSON/tags wrong | Tags on embedded struct | Tag outer or embed with named field for custom marshaling |
| `promoted method` hidden in interface assertion | Outer doesn't implement extra methods | Define all interface methods on outer explicitly |

## Mistakes to Avoid
- **Mistake:** Embedding ≠ inheritance
- **Mistake:** Pointer vs value embed
- **Mistake:** JSON serialization
- **Mistake:** Testing mocks

## Pros/Cons or Trade-offs
- **Trade-off:** Pure "has-a" with no promotion — use named field `logger Logger` for clarity.
- **Trade-off:** Deep embedding chains — hard to trace method origin; prefer explicit delegation.
- **Trade-off:** Hiding third-party types — embed locks API surface to theirs; wrap with named field + forwarders if stability matters.
