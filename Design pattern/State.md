[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Observer]] [[Design pattern/Command]]

# State

> Object alters behavior when its internal state changes — appears to change class — **Dive Into Design Patterns + campaign wizard Draft → Ready → Launched**.

## Mental model

Wizard/campaign lifecycle: each state allows different operations. `Draft` can edit; `Ready` can launch; `Launched` is mostly read-only. State object implements transitions; context delegates.

```
Draft ──submit──► Ready ──launch──► Launched
  │                  │
  └──fail────────────┴──► Failed
```

| Role | Responsibility |

| **Context** | Holds current state; forwards actions |
| --- | --- |
| **State** | Interface for actions / transitions |
| **Concrete states** | Implement legal ops; set next state on context |

## Standard config / commands

```typescript
interface WizardState {
  name: string;
  edit(ctx: WizardContext, patch: object): void;
  submit(ctx: WizardContext): void;
  launch(ctx: WizardContext): void;
}

class DraftState implements WizardState {
  name = 'draft';
  edit(ctx: WizardContext, patch: object) {
    Object.assign(ctx.data, patch);
  }
  submit(ctx: WizardContext) {
    ctx.setState(new ReadyState());
  }
  launch() {
    throw new Error('Submit before launch');
  }
}

class ReadyState implements WizardState {
  name = 'ready';
  edit() {
    throw new Error('Locked — revert to draft first');
  }
  submit() {
    /* already ready */
  }
  launch(ctx: WizardContext) {
    ctx.setState(new LaunchedState());
  }
}

class WizardContext {
  constructor(public state: WizardState, public data: Record<string, unknown> = {}) {}
  setState(s: WizardState) {
    this.state = s;
  }
  edit(patch: object) {
    this.state.edit(this, patch);
  }
  submit() {
    this.state.submit(this);
  }
  launch() {
    this.state.launch(this);
  }
}
```

### vs Strategy

| | State | Strategy |
| --- | --- | --- |
|--|
| Who chooses | Often self-transitions inside states | Caller / config injects |
| Lifetime | Changes over object life | Usually stable per operation |
| Focus | Lifecycle legality | Algorithm variant |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Illegal ops succeed | Missing throws in state | Explicit reject in each concrete state |
| State lost after restart | Only in memory | Persist `state.name` + rehydrate |
| Giant switch on status string | State pattern abandoned | Restore state objects or transition table |
| Transition without event | Hidden `setState` | Only states call `setState` |

## Gotchas

> [!WARNING]
> Persisted enums + in-memory State objects drift — always rehydrate from stored status on load.

- Optional: pair with [[Design pattern/Memento]] for draft undo snapshots.
- UI wizards often need Mediator for step widgets — State owns lifecycle, Mediator owns widget chatter.

## When NOT to use

- Two statuses and one transition — a boolean / enum is enough.
- Behavior does not depend on status — Strategy or plain functions.

## Related

[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Observer]] [[Design pattern/Command]] [[Design pattern/Memento]]
