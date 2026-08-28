Application layer needs a capability, the application doesn't want to know about a particular video provider. It needs "Something that can generate a video."

So the application layer defines an interface

```go
type VideoGenerator interface {
    Generate(prompt string) (string, error)
}
```

Infrastructure provides the implementation, Infrastructure implements the interface
```go
type EvatorVideoGenerator struct {
    client *EvatorClient
}

func (e *EvatorVideoGenerator) Generate(
    prompt string,
) (string, error) {

    // Call Evator API
}
```

### When Infrastructure define the interface

```go
// infrastructure/
type EvatorClient interface {
    GenerateVideo(...)
}
```
- Now the interface is shaped around External service technology. But the application doesn't actually care about Evator. it cares about the **Business capability** "I need a video generator.". That is why the application should therefore define the abstraction around **its own need**

At Application Layer:
```go
type VideoGenerator interface {
    Generate(prompt string) (string, error)
}
```

> [!INFO]
> Infrastructure holds the interface and implementation for the application layer to orchestrate the external service.

> [!INFO]
> The Application Layer defines interfaces (ports) for the external capabilities it needs. The infrastructure Layer provides concrete implementations (adapters) of those interfaces, allowing the Application Layer to orchestrate external services without knowing their implementation details.

What the **port and adapter** is used: "That's the **separation of the business/use-case orchestration from technology-specific implementation**"
Port -> what the application needs.
Adapter -> how infrastructure satisfies that need.

[[Application Layer Code Implementation]]