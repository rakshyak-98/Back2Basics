[[Design pattern]] [[Design pattern/Template Method]] [[Design pattern/Command]]

# Strategy pattern

> Strategy defines a family of algorithms, encapsulates each one, and makes them interchangeable — so the client picks behavior at runtime without conditional branches in the hot path.

```txt
        Strategy pattern ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Strategy tests swapping algorithms at runtime without if/else forests

## Sources
- Gamma et al., *Design Patterns* (Strategy) — deep-dive

## Key Concepts
```
Context → Strategy interface → ConcreteStrategyA / B
```

- **Note:** Context calls `strategy.execute(data)`

## Technical Details
- Payment processing: `PaymentStrategy` with `pay(amount)`
- Checkout holds a strategy reference.

```typescript
class Checkout {
  constructor(private strategy: PaymentStrategy) {}
  pay(amount: number) { this.strategy.pay(amount) }
}
```

## Mistakes to Avoid
- **Mistake:** Strategy per tiny variation — functions or lambdas may be enough
- **Mistake:** Context must expose all data strategies need

## Comparison
- **vs Template Method**

| | Strategy | Template Method |
|---|----------|-----------------|
| Mechanism | Composition (interface) | Inheritance (override hooks) |
| Runtime swap | Easy | Harder (subclass fixed) |
| Granularity | Whole algorithm | Fixed skeleton, variable steps |


### Use cases
- Multiple algorithms for one job (compression, routing, pricing rules).
- Eliminating `switch` on type codes in business logic.
