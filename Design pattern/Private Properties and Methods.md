[[Design pattern]]

# Private Properties and Methods

> Private Properties and Methods — just a name given to the public methods that have access to the private member.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Private Properties and Methods is a design idea — I trade something off and I can name the failure mode.


```javascript
function Gadget(){
	this.name = "iPod";
	this.stretch = function(){
		return "iPad";
	}
}
var toy  = new Gadget();
toy.stretch(); // stretch() is public
```
>[!INFO] doesn't have special syntax for private members. You can implement them using closure.
``` javascript
function Gadget(){
	var name = "iPod";
	this.getName = function(){
		return name;
	}
}
var toy = new Gadget();
toy.name; // undefined
toy.getName(); // iPod
```
#### Privileged Methods
- just a name given to the public methods that have access to the private member.
>[!WARNING] When you're directly returning a private variable from a privileged method this variable happens to be an object or array, then outside code can modify the private variable because it's passed by reference.
- solve this by returning a new object containing only some of the data that could be interesting to the consumer of the object.
#### Object Literals and Privacy

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Private Properties and Methods** | Core idea of this note | “I can explain Private Properties and Methods without jargon.” |
| **scalability** | Handle more load | “Scale reads and writes differently.” |
| **availability** | Stay up on failure | “Redundancy plus health checks.” |
| **consistency** | Same data everywhere | “Pick C or A under partition.” |

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

- Don’t over-design a CRUD app into Kafka+K8s on day one.

---

## Related

[[Design pattern]]
