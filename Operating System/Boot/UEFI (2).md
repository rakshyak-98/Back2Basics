[[Boot]]

# UEFI (2)

> UEFI (2) — this partitioning schema is compatible with older BIOS systems. If you plan to boot from the USB on a machine that uses Legacy BIOS, MBR

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

### MBR
- this partitioning schema is compatible with older BIOS systems. If you plan to boot from the USB on a machine that uses Legacy BIOS, MBR is the appropriate choice.
### GPT
- This is designed for UEFI (Unified Extensible Firmware Interface) systems. If you are using a modern computer that supports UEFI, GPT is the better option.
- It includes redundancy and better data protection features. GPT stores multiple copies of the partitioning and boot data across the disk, which helps in recovery if the data becomes corrupted. This is a significant advantage over MBR, which stores this information in a single location.

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
