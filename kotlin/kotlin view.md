[[kotlin]]

# kotlin view

> kotlin view — binding is a ViewBinding object that provides type-safe access to UI element from your layout XML file.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

`binding` is a ViewBinding object that provides type-safe access to UI element from your layout XML file.
> [!INFO]
> Instead of using `findViewById()`, you use `binding.viewName` to access views
```kotlin
val progressBar = findViewById<ProgressBar>(R.id.progressBar);
progressBar.visibility = View.GONE
binding.progressBar.visibility = View.GONE; // Direct access
```
### Recycler View
A Recycler View is a container that displays a list of items on the screen efficiently. It `recycles` views as you scroll.

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
