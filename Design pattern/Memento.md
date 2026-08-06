[[Design pattern]] [[Design pattern/State]] [[Design pattern/Command]]

# Memento

> Capture and restore an object's internal state without exposing it — undo/draft snapshots — **Dive Into Design Patterns + campaign draft memento**.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Originator (draft) creates an opaque memento; caretaker (history stack) stores it. Restore returns the draft to a prior snapshot without caretaker reading fields.

```
Draft (originator) ──createMemento──► Memento ──stored by──► History
                 ◄──restore──────────┘
```

## Standard config / commands

```typescript
type DraftSnapshot = Readonly<{ name: string; budget: number; goalId: string }>;

class CampaignDraft {
  constructor(public data: { name: string; budget: number; goalId: string }) {}

  save(): DraftSnapshot {
    return Object.freeze({ ...this.data });
  }

  restore(m: DraftSnapshot) {
    this.data = { ...m };
  }
}

const history: DraftSnapshot[] = [];
const draft = new CampaignDraft({ name: '', budget: 0, goalId: '' });

function checkpoint() {
  history.push(draft.save());
}
function undo() {
  const m = history.pop();
  if (m) draft.restore(m);
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Undo leaks private fields | Caretaker reads memento | Keep snapshot opaque / readonly |
| Memory blowup | Unbounded history | Cap stack; persist to disk |
| Partial restore | Nested objects shared by ref | Deep clone on save |

## Gotchas

> [!WARNING]
> …

## When NOT to use

- Full event sourcing already provides replay — don't dual-write mementos.
- Need undo of side-effects on server — [[Design pattern/Command]] with compensating `undo()`.

## Related

[[Design pattern]] [[Design pattern/State]] [[Design pattern/Command]]
