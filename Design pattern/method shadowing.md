[[java]] [[golang]] [[Design pattern]]

# Method shadowing (embedding / inheritance)

> Same-named method on outer and inner type — **which implementation runs depends on the static type of the reference**, not the "logical" OOP hierarchy; source of subtle bugs in Go embedding and Java hiding.

## Mental model

**Overriding (Java virtual methods)** — dynamic dispatch on runtime type.

**Shadowing / hiding** — inner and outer both define same method; caller resolution depends on language rules:

```
Go embed:     var c Car; c.Start() → Car.Start if defined, else promoted Engine.Start
Java static:  Child.hide() hides Parent.hide — reference type picks method
Java field:   Child.x shadows Parent.x — no polymorphism on fields
```

Go: embedding promotes methods; if outer defines `Log`, it **replaces** promoted `Logger.Log` for `Car` receivers — not a runtime override chain.

Java: instance method **override** needs `@Override` + same signature; **hide** if static or mismatched signature.

## Standard config / commands

### Go — embed + override

```go
type Logger struct{}
func (Logger) Log(msg string) { fmt.Println("logger:", msg) }

type Server struct {
    Logger
    name string
}

func (s Server) Log(msg string) {
    fmt.Printf("server[%s]: %s\n", s.name, msg)
}

s := Server{name: "api"}
s.Log("up")              // Server.Log
s.Logger.Log("debug")    // explicit inner — Logger.Log
```

### Go — interface embed

```go
type ReadOnly interface { Read(p []byte) (n int, err error) }
type ReadWrite struct {
    io.ReadWriter // embed interface — must assign concrete impl
}
```

### Java — override vs hide

```java
class Parent {
    static void greet() { System.out.println("parent"); }
    void instance() { System.out.println("parent inst"); }
}

class Child extends Parent {
    static void greet() { System.out.println("child"); } // hides
    @Override
    void instance() { System.out.println("child inst"); } // overrides
}

Parent p = new Child();
p.greet();    // "parent" — static, compile-time type Parent
p.instance(); // "child inst" — virtual dispatch
```

### Java — field shadowing (avoid)

```java
class Parent { int x = 1; }
class Child extends Parent { int x = 2; }
Parent p = new Child();
System.out.println(p.x); // 1 — fields not virtual
```

### Kotlin — override required

```kotlin
open class Base { open fun foo() = 1 }
class Derived : Base() {
    override fun foo() = 2
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong `Log`/helper called | Go promoted vs outer method | Qualify embed `s.Logger.Log` or rename |
| Java "override" doesn't run | Method static / private / wrong sig | Remove static; match signature; add `@Override` |
| Unexpected field value | Field shadowing | Rename field; use getter |
| Interface default vs class | Java 8+ default methods | Explicit override in impl |
| LSP violation in tests | Shadowing breaks substitutability | Favor composition over inheritance |

## Gotchas

> [!WARNING]
> **Go is not Java** — no subclass polymorphism on embedded structs; outer method is fixed at compile time for that type.

> [!WARNING]
> **Java static method "override"** — impossible; hides only — confusing stack traces.

> [!WARNING]
> **JSON/API models shadowing** — Lombok `@Data` on hierarchy can expose wrong property if fields shadow.

## When NOT to use

- **Inheritance to reuse one method** — prefer explicit delegation ([[golang/go embedding]] with named field).
- **Shadowing fields intentionally** — code smell; rename for readability.

## Related

[[java]] [[golang]] [[Static Members]] [[golang/go embedding]]
