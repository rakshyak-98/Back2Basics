[[Descriptive/JavaScript/constructor function]] [[Descriptive/JavaScript/function]] [[javascript]] [[Design pattern/Static Members]]

# `new` operator

> Creates object, sets prototype, runs constructor with fresh `this`, returns instance — **ECMAScript `[[Construct]]`**.

## Mental model

`new Constructor(args)` is syntactic sugar for a fixed sequence — no magic keyword beyond this algorithm:

```
1. Let obj = OrdinaryObjectCreate(Constructor.prototype)
2. Evaluate Constructor with this = obj and arguments
3. If result is Object, return it; else return obj
```

```
new User('Ada')
   │
   ├─ empty object
   ├─ link [[Prototype]] → User.prototype
   ├─ User.call(obj, 'Ada')
   └─ return obj (unless User returns different object)
```

Works on **any** function with a `prototype` object — convention marks "constructors" by naming (`PascalCase`).

## Standard config / commands

### Manual equivalent (understanding only)

```javascript
function myNew(Constructor, ...args) {
  const obj = Object.create(Constructor.prototype);
  const result = Constructor.apply(obj, args);
  return result instanceof Object ? result : obj;
}
```

### Built-ins with `new`

```javascript
new Date();
new Map([['a', 1]]);
new Error('fail');
new Promise((resolve) => resolve(1)); // rarely use new with Promise factory
```

### `new.target` inside constructor

```javascript
function Base() {
  if (new.target === undefined) {
    throw new TypeError('Must call with new');
  }
}
```

### Class syntax (always use `new`)

```javascript
class Service {
  constructor(port) { this.port = port; }
}
// Service() without new → TypeError in class fields mode
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `TypeError: X is not a constructor` | Arrow fn, or no `.prototype` | Use regular function or class |
| `instanceof` wrong | Cross-realm or manual prototype | `Symbol.hasInstance` or duck typing |
| Constructor returns `{}` | Explicit return object | Remove return or document factory |
| `new` on async function | Not constructable | Use factory async function |
| Subclass forgets `new` | `Reflect.construct` edge case | Always `new Derived()` |

## Gotchas

> [!WARNING]
> `new String(1)` creates object wrapper; `String(1)` returns primitive — subtle `typeof` bugs.

- **`new Array(3)`** creates sparse array with length 3, not `[3]`.
- **Optional `new` on builtins:** `Symbol()` must not use `new`; `BigInt()` same.
- **Minifiers** may break `new.target` checks if constructor inlined incorrectly — rare.

## When NOT to use

- Object literals for simple data: `{ id: 1 }` not `new Object()`.
- Factory functions when callers forget `new` often — export plain function returning object.

## Related

[[Descriptive/JavaScript/constructor function]] [[Descriptive/JavaScript/function]] [[Descriptive/JavaScript/execution context]] [[javascript]]
