- Make the class construction `private` member of the class.
	- prevent direct instantiation. 
	- in typescript, if constructor is `public` multiple instances of the class could be created.

---

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

```js
class Singleton {
	static instance = null;
	static {
		this.instance = new Singleton();
	}
	constructor() {
		if (Singleton.instance) {
			throw new Error("Use Singleton.getInstance()");
		}
	}
}
```