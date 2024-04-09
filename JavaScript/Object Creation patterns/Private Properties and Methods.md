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
```javascript
let myObj = (() => {
	let name = "my, oh my"
	myObj = {
		getName: () => {
			return name;
		}
	}
})

myObj.getName(); // "my, oh my"
```
#### Prototypes and Privacy
>[!INFO]] drawback of the private member when used with constructors is that they are recreated every time the constructor is invoked to create a new object.
- add common properties and methods to the prototype property of the constructor.
- this way the common parts are shared among all the instances created with the same constructor.
#### Private Static Members
- shared by all the objects created with the same constructor function.
- not accessible outside the constructor.