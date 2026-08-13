<!-- note-strategy: concept -->
[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Dependency Injection]] [[System Design/HES Architecture]]

# Bridge pattern

> Bridge pattern — without Bridge, one class dimension multiplies subclasses (BasicRemote+TV, BasicRemote+Radio, …). Bridge splits:

---

## Index

- [[#Mental model]]
- [[#Core idea]]
- [[#Variations / implementations]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#Trade-offs]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Without Bridge, one class dimension multiplies subclasses (`BasicRemote+TV`, `BasicRemote+Radio`, …). **Bridge** splits:

```
        Remote (abstraction)          Device (implementation)
              │                              │
    BasicRemote ────────────────► TV
    ProRemote   ────────────────► Projector
```

Abstraction holds a reference to implementor interface — calls delegate at runtime, not via deep inheritance.

| Role | Responsibility |
|------|----------------|
| **Abstraction** | Client-facing API (`Remote.turnOn()`) |
| **Refined abstraction** | Variants (`ProRemote`) |
| **Implementor** | Interface (`Device`) |
| **Concrete implementor** | `TV`, `Projector` |

## Core idea

…

## Variations / implementations

…

## Standard config / commands

### TypeScript example

```typescript
interface Device {
  powerOn(): void;
  powerOff(): void;
}

class TV implements Device {
  powerOn() { console.log('TV on'); }
  powerOff() { console.log('TV off'); }
}

class Remote {
  constructor(protected device: Device) {}
  toggle() {
    // simplified — real code tracks state
    this.device.powerOn();
  }
}

class ProRemote extends Remote {
  mute() { console.log('mute via', this.device); }
}

const remote = new ProRemote(new TV());
remote.toggle();
```

### When to reach for Bridge

- Multiple **UI skins** over same **backend driver**
- Cross-platform rendering (Skia versus CoreGraphics)
- Payment methods × checkout flows without class explosion

### vs similar patterns

| Pattern | Difference |
|---------|------------|
| **Adapter** | Makes incompatible interface work — retrofit |
| **Bridge** | Designed split upfront — parallel hierarchies |
| **Strategy** | Swap algorithm; usually one dimension |
| **State** | Object changes behavior with internal state |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Class explosion returns | Inheritance instead of compose | Inject implementor interface |
| Abstraction leaks impl types | `instanceof TV` in Remote | Keep Remote on `Device` API only |
| Duplicate code in implementors | Shared logic | Extract helper module, not mega base class |
| Testing pain | Hard-coded `new TV()` | [[Design pattern/Dependency Injection]] for Device |
| Wrong implementor at runtime | Wiring in factory | Central DI container / factory map |

## Gotchas

> [!WARNING]
> Bridge adds indirection — don't introduce for two fixed variants that will never multiply.

- **Naming confusion:** "bridge" in networking ([[Networking/BGP]]) is unrelated.
- **Refined abstraction** can re-introduce coupling if it downcasts implementors.
- **Serialization** of abstraction may drop implementor reference — reconstruct via type tag.

## Trade-offs

| Gain | Cost |
|------|------|
| … | … |

## When NOT to use

- Single platform, single backend — concrete class is fine.
- One-off adapter to legacy API — use Adapter pattern.

## Related

[[Design pattern/Command]] [[Design pattern/Dependency Injection]] [[Design pattern/Adapter]] [[Design pattern/Decorator]] [[Design pattern]] [[System Design/HES Architecture]]
