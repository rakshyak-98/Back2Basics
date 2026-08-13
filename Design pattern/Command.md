[[Design pattern]] [[Design pattern/Memento]] [[Design pattern/Strategy pattern]]

# Command

> Command encapsulates a request as an object — so you can queue, log, undo, and wire requests to handlers without the invoker knowing operation details.

## Structure

```
Invoker → Command.execute()
              ↓
         Receiver (does real work)

ConcreteCommand holds Receiver + parameters
```

## Undo / redo

Store executed commands; `undo()` reverses `execute()` if command stores enough state (often paired with [[Design pattern/Memento]]).

## Example uses

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

## When to use

- Decouple UI buttons from business operations.
- Transactional workflows with rollback.
- Remote invocation (command object serialized to message).

## Pitfalls

- Command explosion — group related ops or use parameterized commands.
- Undo without inverse operations — need snapshots ([[Design pattern/Memento]]).

## Sources

- Gamma et al., *Design Patterns* (Command)
- [Command pattern — Wikipedia](https://en.wikipedia.org/wiki/Command_pattern)
