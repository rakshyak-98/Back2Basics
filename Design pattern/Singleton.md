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
			return instance;
		}
		instance = this;
	}
})
```