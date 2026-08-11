[[Design pattern]]

# OOPS

> OOPS — block of memory created when the constructor of a function is invoked.

---

## Mental model

**Say it in one breath:** OOPS is a design idea — I trade something off and I can name the failure mode.


##### Constructors
- special type of member function.
- initialize an object.
- block of memory created when the constructor of a function is invoked.
##### default constructor
- no return type
- no input argument.
### UML diagram
Unified Modeling Language
- DIPD - **Design Implementations Process Design**
	D - consists of classes, interfaces
	implementations -
	Process -
	Design -
- `+` public
- `-` private
- `#` protacted
| ClassName | Employee |
| ----------- | ----------- |
| Class attribute | Name GroupId |
| Class operations | `getAdd()`, `getSet()` |
- visual the system
- documentation
1. timing
2. relationships
3. diagrams
#### things
| Structural | Behavioral | Grouping |
| ------------- | ---------- | ---------- |
| static part of model | Dynamic part of UML model | Grouping elements of UML model together |
| | passing message from one class to another | gathering structure and behavioral thing |
- class, interface


---

## Standard config / commands

```bash
# sketch
# actors, data stores, failure domains
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hot key / hotspot | metrics by key | Shard or cache |
| Cascading failure | timeouts/bulkheads | Add limits and backoff |
| Split brain | fencing / quorum | Use consensus or single writer |

---

## Gotchas

> [!WARNING]
> Draw the failure mode before the happy path.

---

## When NOT to use

- Don’t over-design a CRUD application into Kafka+K8s on day one.

---

## Related

[[Design pattern]]
