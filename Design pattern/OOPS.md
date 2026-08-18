[[Design pattern]] [[Design pattern/Singleton]] [[Design pattern/Private Properties and Methods]]

# OOPS

> Object-oriented programming groups data and behavior in classes — constructors allocate instances, visibility controls access, and UML documents structure.

## Mental model

**Say it in one breath:** A class bundles state (fields) and behavior (methods); a constructor runs when you create an instance and initializes memory for that object.

### Constructors

- Special member functions that **initialize** an object when `new` (or equivalent) runs.
- A **default constructor** takes no arguments and sets sensible initial state.

### UML (Unified Modeling Language)

Visual notation for classes, relationships, and behavior.

| Symbol | Visibility |

| `+` | public |
| --- | --- |
| `-` | private |
| `#` | protected |

| UML element | Role |

| Structural | Static parts — classes, interfaces |
| --- | --- |
| Behavioral | Dynamic parts — messages, sequences |
| Grouping | Packages that group related elements |

## Standard config / commands

```text
ClassName

- privateField: Type
+ publicMethod(): ReturnType
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Uninitialized fields | Constructor path | Ensure all fields set in constructor |
| Subclass cannot access member | Visibility | Widen to `protected` or expose getter |
| Diagram out of sync with code | UML vs implementation | Regenerate or drop stale diagrams |

## Gotchas

> [!WARNING]
> **Inheritance depth** — deep hierarchies are hard to change; favor composition.

## When NOT to use

- **Data-only pipelines** — plain functions and records may be simpler than class trees.

## Related

[[Design pattern]] [[Design pattern/Singleton]] [[Descriptive/UML diagram]]
