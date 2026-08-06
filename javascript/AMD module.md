[[javascript]]

# AMD module

> One-line: what / why for **AMD module** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- Asynchronously Module Definition
- JavaScript module format designed for browser based environment that require asynchronous loading of modules.
- Uses a `define` function to declare modules and their dependencies.
- Provide `require` function to load modules when needed.
```javascript
define(['dependency1', 'dependency2'], function(dep1, dep2) {
	return {
		someMethod: function(){
			// Module functionality
			dep1.action();
			dep2.action();
		}
	}
})
```
```javascript
require(['myModule'], function(myModule){
	myModule.something();
})
```

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
