[[Common Naming terms.md]]

# Common Naming terms

> Common Naming terms — daemon: Used for background processes that run continuously.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Common Naming terms — plain job, how I run it, how I know it’s broken.


Daemon: Used for background processes that run continuously.
Monitor: Used for agents that monitor system states or resources.
Service: For system services or processes.
Task: Represents a unit of work or a scheduled task.
Process: Indicates a running task or purpose.
Handler: For handling specific actions or events.
Controller: Manages or controls specific operations.
Manager: Manages resources or tasks.
Agent: Represents a software agent or autonomous entity.
Proxy: Represents an intermediary or agent that forwards requests.
Monitor: For agents that observe network traffic or performance.
Router: Agents that handle routing or path selection in networks.
Firewall: Represents network security agents.
Sensor: For monitoring network conditions or status.
Controller: Used for managing network traffic or security rules.
Collector: Agents that collect data, such as logs or metrics.
Agent: A general term for agents performing network tasks.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Common Naming terms** | Core idea of this note | “I can explain Common Naming terms without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[Common Naming terms.md]]
