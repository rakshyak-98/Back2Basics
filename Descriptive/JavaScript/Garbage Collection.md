## Garbage collection
- memory management in JavaScript is performed automatically and invisibly to us.
- the garbage collector tries to run only while the CPU is idle, to reduce the possible effect on the execution.
### what happens when something is not needed any more? How does JavaScript engine discover it and clean it up?
#### reachability
- _reachable_ values are those that are accessible or usable somehow.
1. There are base set of inherently reachable values (_roots_), that cannot be deleted.
	- currently __executing function__, its local variables and parameters.
	- other function on the __current chain__ of nested calls, their local variables and parameters.
	- global variables
2. if it's reachable from a _root_ by a reference or by a chain of references.
	- if there's an object in a global variable, and that object has a property referencing another object, that object is considered reachable. And those that it references are also reachable.
	
> [!INFO] there are background processes in the JavaScript engine that is called [garbage collector](). It monitors all objects and removes those that have become unreachable.

> [!INFO] only incoming references can make an object reachable.
#### internal algorithms
- the garbage collector takes roots and "marks" (remembers) them.
- then it visits and "marks" all references from them.
- then it visits marked objects and marks their references. All visited objects are remembered, so as not to visit the same object twice in the future.
- so on until every reachable (from the roots) references are visited.
- all objects except marked ones are removed.
[A tour of V8: Garbage Collection](https://jayconrod.com/posts/55/a-tour-of-v8-garbage-collection)
