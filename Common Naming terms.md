[[Linux Process Theory]] [[Proxy]] [[Design pattern]] [[Networking]]

# Common Naming terms

> Common naming terms — short vocabulary for background workers, agents, and control-plane roles you’ll see in code and ops.

## Interview Relevance
Clear naming shows system literacy: daemon vs service vs agent, proxy vs gateway, controller vs manager. Interviewers notice when you use these words precisely.

## Sources
- [Wikipedia — Daemon (computing)](https://en.wikipedia.org/wiki/Daemon_(computing)) — overview
- [Wikipedia — Software agent](https://en.wikipedia.org/wiki/Software_agent) — overview

## Core Definition
These are conventional role names for processes and components. They are not formal standards — consistency inside a codebase matters more than any single dictionary — but industry usage clusters around the meanings below.

## Key Concepts
- **Daemon:** Long-running background process (often no controlling terminal), e.g. `sshd`, `dockerd`.
- **Service:** Unit of functionality managed by an init system or platform (systemd unit, K8s Service is a different meaning — networking abstraction).
- **Process / task:** Running instance of a program; “task” also means a scheduled unit of work.
- **Handler / controller:** Code that reacts to an event or reconciles desired vs actual state (API handler vs control-loop controller).
- **Manager / agent:** Manager orchestrates; agent runs locally and reports or enforces (monitoring agent, backup agent).
- **Proxy / router / firewall:** Intermediary forwarder; path selector; policy enforcement on traffic.
- **Sensor / collector / monitor:** Observe conditions; gather metrics/logs; watch health.

## Technical Details
| Term | Typical job |
|------|-------------|
| Daemon | Stay up; serve or watch in the background |
| Service | Operated lifecycle (start/stop/restart) + API |
| Agent | Local presence of a central system |
| Proxy | Terminate or forward on behalf of clients ([[Proxy/Reverse Proxy]]) |
| Controller | Reconcile state (K8s controllers, MVC controllers — different layers) |
| Worker / task | Execute jobs from a queue |

Disambiguate in interviews: “Kubernetes Service” ≠ “systemd service” ≠ “micro-service.”

## Real-World Applications
Naming a component `payment-agent` on each host that talks to a central `payment-manager` sets expectations: local, possibly offline-tolerant, reports upward. A `*-proxy` suggests traffic path, not business logic.

## Pros/Cons or Trade-offs
- **Pro:** Shared mental model across teams and diagrams.
- **Con:** Overloaded words (service, agent, controller) cause confusion without context.

## Comparison
vs [[Design pattern]] names (Proxy, Facade): pattern names describe *structure*; these ops names describe *runtime role*. Related: [[Linux Process Theory]] for real process behavior.

## Mistakes to Avoid
- Using “daemon,” “service,” and “agent” interchangeably in one design doc.
- Naming everything `*Manager` until nothing has a clear boundary.
- Assuming interviewers share your company’s private naming dialect without defining it.
