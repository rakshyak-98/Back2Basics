[[Design pattern]] [[Design pattern/Memento]] [[Design pattern/Strategy pattern]]

# Command

> Command encapsulates a request as an object — so you can queue, log, undo, and wire requests to handlers without the invoker knowing operation details.





## Interview Relevance
Command questions encapsulate requests as objects — queues, undo, logging, and decoupling invoker from receiver.

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
**Undo / redo**

Store executed commands; `undo()` reverses `execute()` if command stores enough state (often paired with [[Design pattern/Memento]]).

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

## Real-World Applications
- Decouple UI buttons from business operations.
- Transactional workflows with rollback.
- Remote invocation (command object serialized to message).

## Mistakes to Avoid
- Command explosion — group related ops or use parameterized commands.
- Undo without inverse operations — need snapshots ([[Design pattern/Memento]]).
