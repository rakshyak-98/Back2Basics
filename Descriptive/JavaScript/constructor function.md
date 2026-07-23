[[Descriptive/JavaScript/new]] [[Descriptive/JavaScript/function]] [[javascript]] [[Design pattern/Static Members]]

# Constructor function

> Pre-ES6 factory for instances — regular function + `new` wires prototype and `this` — **ECMAScript object model**.

## Mental model

A **constructor function** is a normal function intended to be called with `new`. It creates an object, links prototypes, runs the body with `this` bound to that object, and returns it (unless overridden).

```
new Person('Ada')
    │
    ├─► create empty object {}
    ├─► obj.[[Prototype]] = Person.prototype
    ├─► call Person with this = obj
    └─► return obj (unless Person returns another object)
```

| Era | Pattern |
|-----|---------|
| ES5 | `function User() { this.name = … }` |
| ES6+ | `class User { constructor() { … } }` — syntactic sugar over prototypes |
| Factory (no `new`) | `function createUser() { return { … }; }` — no prototype chain |

Constructors are **not** special to the engine — only `new` gives them constructor semantics.

## Standard config / commands

### ES5 constructor + prototype methods

```javascript
function User(name) {
  if (!(this instanceof User)) {
    throw new TypeError('Use new User()');
  }
  this.name = name;
}

User.prototype.greet = function () {
  return `Hi, ${this.name}`;
};

const u = new User('Ada');
```

### ES6 class (preferred today)

```javascript
class User {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Hi, ${this.name}`;
  }
}
```

### Guard against forgetting `new` (legacy libs)

```javascript
function User(name) {
  if (!(this instanceof User)) return new User(name);
  this.name = name;
}
```

### Subclassing (ES6)

```javascript
class Admin extends User {
  constructor(name, role) {
    super(name); // must before this
    this.role = role;
  }
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `TypeError: Cannot set property 'x' of undefined` | Called without `new` | Use `new` or class syntax |
| Methods missing on instance | Method on constructor, not prototype | Move to `Constructor.prototype.method` |
| `instanceof` false across iframes | Different realm prototypes | Duck-type or Symbol branding |
| Subclass `this` before `super` | ES6 class rules | Call `super()` first in derived constructor |
| Constructor returns plain object | Explicit `return { … }` | Only return object if intentional; else omit return |

## Gotchas

> [!WARNING]
> Arrow functions cannot be constructors — no `prototype`, `new` throws.

- **`new.target`:** detects whether function invoked via `new` (useful in dual factory/constructor APIs).
- **Shared state bug:** `function User() { this.tags = []; }` is per-instance; `User.prototype.tags = []` is shared.
- **Minification + `instanceof`:** breaking constructor names can confuse debuggers, not semantics.

## When NOT to use

- Simple data holders — plain objects or `Object.create(null)` suffice.
- Heavy inheritance hierarchies — favor composition or factory functions.
- TypeScript codebase — `class` + interfaces gives better tooling.

## Related

[[Descriptive/JavaScript/new]] [[Descriptive/JavaScript/function]] [[Descriptive/JavaScript/execution context]] [[javascript]]
