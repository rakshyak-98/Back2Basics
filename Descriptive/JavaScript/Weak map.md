- additional storage of data for objects which are store or managed at another place.
- the main area of application is an addition data storage.
- keys must be objects, not primitive value.
- does not support iteration and methods `keys` `values` `entries`.
- absence of iterations, and the inability to get all current content.

### why such limitation?
- for technical reasons, the current element count of a `WeakMap` is not known. The engine may have cleared it up or not, or did it partially. For that reason, methods that access all keys or values are not supported.

usually, properties of an object or elements of an array or another data structure are considered reachable and kept in memory while that data structure is in memory.

For instance, if we put an object into an array, then while the array is alive, the object will be alive as well, even if there are no other references to it.

```jsx
let john = {name: "John"};
let array = [john];

john = null; // overwrite the reference

// the object previously referenced by john is stored inside the array
// therefore it won't be garbage-collected
// we can get it as array[0]
```

```jsx
let john = {name: "John"};
let array = [john];
john = null; // overwrite the reference

// john is stored inside the map,
// we can get it by using map.keys();
```

weak map is fundamentally different in this aspect.
```jsx
let weakMap = new WeakMap();
let obj = {};
weakMap.set(obj, "ok"); // works fine

// can't use a string as the key
weakMap.set("test", "Wrong"); // Error
```

```jsx
let john = {name: "john"};
let weakMap = new WeakMap();
weakMap.set(john, "...");
john = null; // overwrite the reference
// john is removed from memory;
```