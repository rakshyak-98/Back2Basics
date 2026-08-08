[[Boot]]

# Extensible Firmware interface (efi)

> Extensible Firmware interface (efi) — EFI servers as a modern replacement for the traditional BIOS (Basic Input/Output System) firmware interface.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- EFI servers as a modern replacement for the traditional BIOS (Basic Input/Output System) firmware interface.
- it initializes hardware components during the boot process and provides an interface for the operating system.
- support large hard drives (over 2 TB) due to using the [[GPT (GUID Partation Table)]] instead of [[MBR(Master Boot Record)]]
- provides a flexible architecture that can support various operating system and device drivers.
> [!INFO] modern implementations of EFI are often referred to as [[OS Boot/UEFI|UEFI]]

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
