[[flutter]]

# flutter debugging

> flutter debugging — short field notes on what it is and how to use it.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** flutter debugging — short field notes on what it is and how to use it.

### Process description
| Process           | Purpose                                           |
| ----------------- | ------------------------------------------------- |
| `dart:dartdev_ao` | Dart CLI launcher (`dart` command infrastructure) |
| `dart:flutter_to` | Flutter tool (`flutter run`, `flutter build`)     |
| `adb`             | Android Debug Bridge command                      |
| `dart:dartdev_ao` | Another Dart CLI helper process                   |
| `adb`             | Another ADB invocation                            |
| `dart:frontend_s` | Dart frontend server (compiler)                   |


---

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

[[flutter]]
