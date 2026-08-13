[[Design pattern]] [[Design pattern/Adapter]] [[Design pattern/Decorator]]

# Facade

> Facade offers a single simplified entry point to a subsystem — hiding many classes, protocols, and error modes behind one coordinated call.

## Example

Home theater: `watchMovie()` turns on projector, amp, player, dims lights — instead of the client orchestrating five objects.

```
Client → Facade.watchMovie()
            → Subsystem classes (many steps, order matters)
```

Facade does not block direct subsystem access; it **reduces** what most callers need to know.

## vs Adapter

Facade **simplifies** a subsystem; Adapter **changes** interface shape for one object.

## When to use

- Legacy modules with tangled APIs.
- Onboarding layer for complex SDKs (cloud deploy, media pipeline).
- Application service layer over repositories + messaging.

## Pitfalls

- God facade that knows everything — split by use case (`BillingFacade`, `OnboardingFacade`).
- Facade that becomes the only path and hides useful subsystem features without documentation.

## Sources

- Gamma et al., *Design Patterns* (Facade)
- [Facade pattern — Wikipedia](https://en.wikipedia.org/wiki/Facade_pattern)
