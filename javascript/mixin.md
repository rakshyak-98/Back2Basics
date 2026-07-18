- class containing methods that can be used by other classes without a need to inherit from it.
```javascript
let sayHiMixin = {
	sayHi() {
		console.log(`Hello ${this.name}`);
	},
	sayBya() {
		console.log(`Byte ${this.name}`);
	}
}

class User{
	constructor(name){
		this.name = name;
	}
}

// no inheritance, simple method copying.
Object.assign(User.prototype, sayHiMixin);

new User("John").sayHi();
```

> [!NOTE] `super` looks for parent methods in `[[HomeObject]].[[Prototype]]`

```javascript
let sayMixin = {
	say(phrase){
		console.log(phrase);
	}
}

let sayHiMixin = {
	__proto__: sayMixin,

	sayHi(){
		super.say(`Hello ${this.name}`);
	},

	sayBye(){
		super.say(`Hello ${this.name}`);
	}
}

class User{
	constructor(name){
		this.name = name;
	}
}

Object.assign(User.prototype, sayHiMixin);

new User("Dude").sayHi();
```

