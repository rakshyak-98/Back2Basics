[[Design pattern]] [[Design pattern/Static Members]] [[Design pattern/OOPS]]

# method shadowing

> Method shadowing (and field hiding) occurs when a subclass defines a static method or field with the same name as the parent — the subclass does **not** override the parent's static member; each type resolves its own version.

## Interview Relevance

Method shadowing checks name-hiding across inheritance — override versus hide, and surprising dispatch.

## Sources

- Java Language Specification — hiding vs overriding — deep-dive

## Technical Details

**Static vs virtual override**

```java
class Parent {
  static void greet() { System.out.println("parent"); }
  void hello() { System.out.println("parent"); }
}
class Child extends Parent {
  static void greet() { System.out.println("child"); }  // hides, not overrides
  @Override void hello() { System.out.println("child"); } // overrides
}
```

| Call | Result |
|------|--------|
| `Child.greet()` | `child` |
| `Parent.greet()` | `parent` |
| `Parent p = new Child(); p.greet()` | `parent` (static resolved by reference type) |
| `p.hello()` | `child` (virtual dispatch) |

**Field hiding**

Subclass field with same name as parent hides the parent's field — two storage slots exist; access depends on reference type, not object runtime type.

**Why it matters**

- Developers expect "override" behavior and get silent wrong static dispatch.
- Linters flag missing `@Override` on instance methods; static hides are easy to miss.
- Design: avoid static methods in inheritance hierarchies — use instance methods or composition ([[Design pattern/Strategy pattern]]).

**Language variance**

- **Java** — explicit hiding terminology in JLS.
- **C#** — `new` keyword marks intentional hiding.
- **JavaScript** — class fields and methods use prototype chain; different mechanics.
