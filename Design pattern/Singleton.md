<!-- note-strategy: concept -->
[[Design pattern]]

# Singleton

> Singleton — make the class construction private member of the class.

---

## Index

- [[#Mental model]]
- [[#Core idea]]
- [[#Variations / implementations]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#Trade-offs]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Singleton is a design idea — I trade something off and I can name the failure mode.


- Make the class construction `private` member of the class.
	- prevent direct instantiation.
	- in typescript, if constructor is `public` multiple instances of the class could be created.
- Instance in a Static Property
	- caching the singular instance in a static property.
	- drawback that instance is public.
- Instance in a Closure
	- using private static member pattern.
	- rewrite the constructor.
	- drawback is that the rewritten function will lose any properties (prototype) added to it between the moment of initial definition and the redefinition.
```javascript
function Universe(){
	let instance;
	Universe = function(){
		return instance;
	}
	// carry over the prototype properties
	Universe.prototype = this;
	instance = new Universe();
	// reset the constructor pointer
	instance.constructor = Universe;
	return instance;
}
```
```javascript
var Universe
(function(){
	let instance;
	Universe = function(){
		if(instance){


---

## Core idea

…

## Variations / implementations

…

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

## Trade-offs

| Gain | Cost |
|------|------|
| … | … |

## When NOT to use

- Don’t over-design a CRUD app into Kafka+K8s on day one.

---

## Related

[[Design pattern]]
