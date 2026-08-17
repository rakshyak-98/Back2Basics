[[Descriptive/JavaScript/new]] [[Descriptive/JavaScript/function]] [[javascript]] [[Design pattern/Static Members]] [[Descriptive/JavaScript/execution context]]

# Constructor function

> Pre-ES6 factory for instances — regular function + `new` wires prototype and `this` — **ECMAScript object model**.

```txt
        Constructor functi ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Constructor reviews check new, prototypes, and class syntax equivalence.

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** A **constructor function** is a normal function intended to be called with `n…

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

- **Note:** Constructors are **not** special to the engine

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> Arrow functions cannot be constructors — no `prototype`, `new` throws.

- **Mistake:** **`new.target`:** detects whether function invoked via `new` (us…
- **Mistake:** **Shared state bug:** `function User() { this.tags = []
- **Mistake:** **Minification + `instanceof`:** breaking constructor names can …

| Symptom | Check | Fix |
|---------|-------|-----|
| `TypeError: Cannot set property 'x' of undefined` | Called without `new` | Use `new` or class syntax |
| Methods missing on instance | Method on constructor, not prototype | Move to `Constructor.prototype.method` |
| `instanceof` false across iframes | Different realm prototypes | Duck-type or Symbol branding |
| Subclass `this` before `super` | ES6 class rules | Call `super()` first in derived constructor |
| Constructor returns plain object | Explicit `return { … }` | Only return object if intentional; else omit return |

## Pros/Cons or Trade-offs
- Simple data holders — plain objects or `Object.create(null)` suffice.
- Heavy inheritance hierarchies — favor composition or factory functions.
- TypeScript codebase — `class` + interfaces gives better tooling.
