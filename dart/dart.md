[[dart]]

# dart

> One-line: what / why for **dart** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Factory constructor]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

`factory ApiRoomDate.fromJson(...)`
- Factory -> Unlike a normal constructor, a `factory` constructor can return an existing instance or even a subclass. In this context, it's used to return a fully populated `ApiRoomData` object after processing the JSON.
- Map<String, dynamic>  -> This represents the structure of a standard JSON object (keys are Strings, values can by anything)

## Standard config / commands

…

## Factory constructor

- is a specialized constructor that doesn't always create a new instance of its own class.
- while a generative constructor (the standard one) always creates a new object and initializes its fields, a factory constructor gives you more control over the instantiation process.

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
