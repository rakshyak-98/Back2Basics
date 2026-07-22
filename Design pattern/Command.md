[[Design pattern]] [[Design pattern/Bridge]] [[Messaging/Web hooks]] [[Projects/marketplace app]]

# Command pattern

> Encapsulate an action as an object — invoker, undo, queue, and log requests — **GoF + UI/action systems**.

## Mental model

```
Client ──creates──► Command ──passed to──► Invoker ──calls──► Receiver
                         │                      │
                         └── stores params        └── execute() / undo()
```

| Role | Example |
|------|---------|
| **Command** | `TurnOnCommand` |
| **Receiver** | `Bulb` (does real work) |
| **Invoker** | `RemoteController` |
| **Client** | Wires commands to invoker |

Invoker doesn't know concrete receiver — enables macro commands, undo stack, job queues.

## Standard config / commands

### JavaScript reference shape

```javascript
class Bulb {
  turnOn() { console.log('on'); }
  turnOff() { console.log('off'); }
}

class TurnOn {
  constructor(bulb) { this.bulb = bulb; }
  execute() { this.bulb.turnOn(); }
}

class TurnOff {
  constructor(bulb) { this.bulb = bulb; }
  execute() { this.bulb.turnOff(); }
}

class RemoteController {
  execute(command) { command.execute(); }
}

function main() {
  const bulb = new Bulb();
  const remote = new RemoteController();
  remote.execute(new TurnOn(bulb));
  remote.execute(new TurnOff(bulb));
}
```

### Undo stack

```javascript
class MoveCommand {
  constructor(obj, dx, dy) { this.obj = obj; this.dx = dx; this.dy = dy; }
  execute() { this.obj.x += this.dx; this.obj.y += this.dy; }
  undo() { this.obj.x -= this.dx; this.obj.y -= this.dy; }
}

const history = [];
function run(cmd) { cmd.execute(); history.push(cmd); }
function undo() { history.pop()?.undo(); }
```

### Production uses

- **Job queues:** command payload = serializable message ([[Messaging/Web hooks]], SQS)
- **CQRS:** command side separates from read models
- **Text editor** undo/redo stacks
- **Transaction scripts** with compensating actions (saga step)

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Undo inconsistent state | Command not reversible | Store before-snapshot or inverse op |
| Memory leak in history | Unbounded stack | Cap size or persist to disk |
| Duplicate execution | Retry without idempotency | Idempotent command IDs |
| Invoker knows too much | Fat command interface | Narrow to `execute()` only |
| Serialization fails | Closures in command | Data-only command DTOs |

## Gotchas

> [!WARNING]
> **Macro commands** that partially fail need composite rollback — implement `undo` on each sub-command in reverse order.

- **Not the same as event** — command is imperative intent; event is fact that happened.
- **Functional style** — `(state) => newState` reducers are command pattern without classes.
- **Thread safety** — invoker queue must serialize if receiver is shared mutable state.

## When NOT to use

- Simple one-shot function call with no undo/queue/logging — YAGNI.
- Entire app as Command objects — prefer plain functions until undo/queue appears.

## Related

[[Design pattern/Bridge]] [[Design pattern/Dependency Injection]] [[Architectures/Orchestration layer]] [[Messaging/Web hooks]]
