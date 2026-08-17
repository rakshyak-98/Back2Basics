[[Design pattern]] [[Design pattern/Memento]] [[Design pattern/Strategy pattern]]

# Command

> Command encapsulates a request as an object — so you can queue, log, undo, and wire requests to handlers without the invoker knowing operation details.

```txt
        Command ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Command questions encapsulate requests as objects

## Sources
- Gamma et al., *Design Patterns* (Command) — deep-dive

## Key Concepts
```
Invoker → Command.execute()
              ↓
         Receiver (does real work)

ConcreteCommand holds Receiver + parameters
```

## Technical Details
- **Undo / redo:** 

- Store executed commands

- Text editor undo stack.
- Job queues (`Command` per task).
- Macro recording (list of commands replayed).

```typescript
interface Command { execute(): void; undo(): void }
class InsertText implements Command {
  constructor(private doc: Document, private text: string, private pos: number) {}
  execute() { doc.insert(pos, text) }
  undo() { doc.delete(pos, text.length) }
}
```

## Mistakes to Avoid
- **Mistake:** Command explosion
- **Mistake:** Undo without inverse operations

## Real-World Applications
- **Decouple UI:** Decouple UI buttons from business operations.
- **Transactional workflows:** Transactional workflows with rollback.
- **Remote invocation:** Remote invocation (command object serialized to message).
