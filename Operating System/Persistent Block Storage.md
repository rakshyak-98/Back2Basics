[[Operating System]]

# Persistent Block Storage

> Persistent Block Storage — refers to a storage system that retains data even after the associated compute resource (e.g., a virtual machine) is stopped or restarted.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

> [!INFO] Reliable data storage for stateful applications.
- refers to a storage system that retains data even after the associated compute  resource (e.g., a virtual machine) is stopped or restarted.
- it is structured into fixed-sized _blocks_ that application can read or write directly, offering efficient and low-latency access.
- Block Level access: stores data in fixed-size blocks, allowing precise and efficient access.
- Attachable to compute instance: can be attached/detached to virtual machines as needed.
- Scalability: can be resized or adjusted to fit application requirements.
> [!INFO] Backup support: Enables snapshots or backups for data protection.
> [!INFO] High performance for transactional workloads.

## Standard config / commands

…

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
