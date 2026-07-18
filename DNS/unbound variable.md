As unbound variable is a variable that has been referenced in a program but has not been assigned a value before being used. This leads to a runtime error.

```js
console.log(x); // ReferenceError: x is not defined
```

```bash
echo $myvar # no error, but prints nother (undefined variable)
set -u
echo $myvar # Error: unbound variable
```
- Unbound variables occur when you use a variable before assigning a value.