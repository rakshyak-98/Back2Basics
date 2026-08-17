[[Design pattern]] [[Design pattern/Static Members]] [[Design pattern/OOPS]]

# Private Properties and Methods

> Private members hide implementation detail inside a class or module — so invariants stay enforceable and public APIs stay small.





## Interview Relevance
Interviewers ask encapsulation mechanics — language privacy versus convention, and what invariants you protect.

## Sources
- Gamma et al., *Design Patterns* (encapsulation) — deep-dive
- ECMAScript private fields specification — deep-dive

## Technical Details
**Encapsulation**

Callers use public methods; internal representation can change without breaking clients.

```typescript
class BankAccount {
  #balance = 0           // private field (JS)
  deposit(amount: number) {
    if (amount <= 0) throw new Error("invalid")
    this.#balance += amount
  }
}
```

**Language mechanisms**

| Language | Private mechanism |
|----------|-------------------|
| Java | `private`, package-private |
| TypeScript | `private`, `#` fields |
| Python | `_name` convention, `__name` mangling |
| Go | lowercase unexported identifiers in package |
| Rust | `pub` vs private module visibility |

True privacy vs convention — know what your language actually enforces.

**Patterns that rely on privacy**

- [[Design pattern/Memento]] — originator controls memento access.
- [[Design pattern/Singleton]] — private constructor blocks extra instances.
- [[Design pattern/Builder]] — hide partial construction state until `build()`.

## Comparison
**vs protected**

`protected` exposes to subclasses — wider surface, harder to reason about than private + composition.

## Mistakes to Avoid
- Reflection/serialization bypassing privacy.
- Testing private logic directly — test through public behavior or use test-only package access.
- Excessive `friend` or `@VisibleForTesting` — sign of misplaced responsibility.
