[[Design pattern]] [[Design pattern/Template Method]] [[Design pattern/Command]]

# Strategy pattern

> Strategy defines a family of algorithms, encapsulates each one, and makes them interchangeable — so the client picks behavior at runtime without conditional branches in the hot path.

## Structure

```
Context → Strategy interface → ConcreteStrategyA / B
```

Context calls `strategy.execute(data)`; wiring can happen at construction or via setter.

## vs Template Method

| | Strategy | Template Method |
|---|----------|-----------------|
| Mechanism | Composition (interface) | Inheritance (override hooks) |
| Runtime swap | Easy | Harder (subclass fixed) |
| Granularity | Whole algorithm | Fixed skeleton, variable steps |

## Example

Payment processing: `PaymentStrategy` with `pay(amount)` — `CreditCard`, `PayPal`. Checkout holds a strategy reference.

```typescript
class Checkout {
  constructor(private strategy: PaymentStrategy) {}
  pay(amount: number) { this.strategy.pay(amount) }
}
```

## When to use

- Multiple algorithms for one job (compression, routing, pricing rules).
- Eliminating `switch` on type codes in business logic.

## Pitfalls

- Strategy per tiny variation — functions or lambdas may be enough.
- Context must expose all data strategies need — avoid strategies reaching into private context state.

## Sources

- Gamma et al., *Design Patterns* (Strategy)
- [Strategy pattern — Wikipedia](https://en.wikipedia.org/wiki/Strategy_pattern)
