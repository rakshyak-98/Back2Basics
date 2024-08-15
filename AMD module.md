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