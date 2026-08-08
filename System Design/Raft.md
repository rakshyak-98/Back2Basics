[[System Design]]

# Raft

> Raft — a consensus algorithm designed for distributed systems. It enables a cluster of servers (nodes) to agree on a shared state, even in the presence of failures

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#What Problem Does Raft Solve?]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Raft is a consensus algorithm designed for distributed systems. It enables a cluster of servers (nodes) to agree on a shared state, even in the presence of failures, network partitions, or crashes, while maintaining strong consistency.

## Standard config / commands

…

## What Problem Does Raft Solve?

In a distributed system, multiple servers must maintain identical copies of data (replicated logs or state machines). The core challenge is consensus -> ensuring all healthy nodes agree on the same sequence of operations despite failures. Raft provides a reliable, understandable way to achieve this.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
