[[Linux Process Theory]] [[Proxy]] [[Design pattern]] [[Networking]]

# Common Naming terms

> Common naming terms — short vocabulary for background workers, agents, and control-plane roles you’ll see in code and ops.

```txt
        Common Naming term ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Clear naming shows system literacy: daemon vs service vs agent, proxy vs gate…

## Sources
- [Wikipedia — Daemon (computing)](https://en.wikipedia.org/wiki/Daemon_(computing)) — overview
- [Wikipedia — Software agent](https://en.wikipedia.org/wiki/Software_agent) — overview

## Key Concepts
- **Daemon:** Long-running background process (often no controlling terminal), e.g
- **Service:** Unit of functionality managed by an init system or platform (systemd unit, K8…
- **Process / task:** Running instance of a program; “task” also means a scheduled unit of work.
- **Handler / controller:** Code that reacts to an event or reconciles desired vs actual state (API handl…
- **Manager / agent:** Manager orchestrates
- **Proxy / router / firewall:** Intermediary forwarder; path selector; policy enforcement on traffic.
- **Sensor / collector / monitor:** Observe conditions; gather metrics/logs; watch health.


- **Core:** These are conventional role names for processes and components. They are not …

## Technical Details
| Term | Typical job |
|------|-------------|
| Daemon | Stay up; serve or watch in the background |
| Service | Operated lifecycle (start/stop/restart) + API |
| Agent | Local presence of a central system |
| Proxy | Terminate or forward on behalf of clients ([[Proxy/Reverse Proxy]]) |
| Controller | Reconcile state (K8s controllers, MVC controllers — different layers) |
| Worker / task | Execute jobs from a queue |

- Disambiguate in interviews: “Kubernetes Service” ≠ “systemd service” ≠ “micro…

## Mistakes to Avoid
- **Mistake:** Using “daemon,” “service,” and “agent” interchangeably in one de…
- **Mistake:** Naming everything `*Manager` until nothing has a clear boundary
- **Mistake:** Assuming interviewers share your company’s private naming dialec…

## Pros/Cons or Trade-offs
- **Pro:** Shared mental model across teams and diagrams.
- **Con:** Overloaded words (service, agent, controller) cause confusion without context.

## Comparison
- vs [[Design pattern]] names (Proxy, Facade): pattern names describe *structur…


### Use cases
- Naming a component `payment-agent` on each host that talks to a central `paym…
