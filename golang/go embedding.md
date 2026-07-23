[[golang]] [[Design pattern]] [[java]]

# Go embedding (struct and interface)

> Anonymous field embedding — promotes methods and fields for convenient delegation; **not** classical inheritance; conflicts resolve by explicit outer rules.

## Mental model

Embedding places a type inside another **without a field name**. The outer type **promotes** the embedded type's exported methods and fields to the outer type's method set.

```go
type Reader struct { io.Reader }  // embed interface
type Engine struct { hp int }
type Car struct {
    Engine          // promoted: Car.hp, Car methods if any on Engine
    brand string
}
```

Two cases:
1. **Embed struct** — fields and methods promoted; outer can override by defining same method (not shadowing like Java — see [[method shadowing]] in Go context: outer wins on direct call).
2. **Embed interface** — outer satisfies interface if embedded interface is satisfied (implicit delegation pattern).

No virtual dispatch chain — method on outer replaces promoted method when called on outer type.

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ambiguous selector X` | Two embeds expose same field/method | Qualify `outer.A.X`; rename or drop embed |
| Interface not satisfied | Embedded interface nil | Initialize embedded field; implement missing methods on outer |
| Method not promoted | Unexported (lowercase) method | Export method or wrap with exported forwarder |
| Unexpected nil panic | Embedded pointer nil | Use value embed or construct with `&T{}` |
| JSON/tags wrong | Tags on embedded struct | Tag outer or embed with named field for custom marshaling |
| `promoted method` hidden in interface assertion | Outer doesn't implement extra methods | Define all interface methods on outer explicitly |

## Gotchas

> [!WARNING]
> **Embedding ≠ inheritance** — no LSP hierarchy; promoted methods copy by name, outer override is static dispatch.

> [!WARNING]
> **Pointer vs value embed** — `embed *T` promotes pointer-receiver methods; value embed `T` may not promote pointer-only methods on value of outer.

> [!WARNING]
> **JSON serialization** — anonymous embed fields flatten into parent JSON object; can surprise API consumers.

> [!WARNING]
> **Testing mocks** — embedding mock interface in struct is idiomatic but nil embedded interface causes panic on call.

## When NOT to use

- **Pure "has-a" with no promotion** — use named field `logger Logger` for clarity.
- **Deep embedding chains** — hard to trace method origin; prefer explicit delegation.
- **Hiding third-party types** — embed locks API surface to theirs; wrap with named field + forwarders if stability matters.

## Related

[[golang]] [[method shadowing]] [[Design pattern]] [[java]]
