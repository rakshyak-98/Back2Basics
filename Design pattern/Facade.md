[[Design pattern]] [[Design pattern/Adapter]] [[Design pattern/Decorator]]

# Facade

> Facade offers a single simplified entry point to a subsystem — hiding many classes, protocols, and error modes behind one coordinated call.





## Interview Relevance
Facade probes giving callers one simple entry to a messy subsystem — interviewers watch for god-facade smell versus genuine simplification.

## Sources
- Gamma et al., *Design Patterns* (Facade) — deep-dive

## Technical Details
Home theater: `watchMovie()` turns on projector, amp, player, dims lights — instead of the client orchestrating five objects.

```
Client → Facade.watchMovie()
            → Subsystem classes (many steps, order matters)
```

Facade does not block direct subsystem access; it **reduces** what most callers need to know.

## Real-World Applications
- Legacy modules with tangled APIs.
- Onboarding layer for complex SDKs (cloud deploy, media pipeline).
- Application service layer over repositories + messaging.

## Comparison
**vs Adapter**

Facade **simplifies** a subsystem; Adapter **changes** interface shape for one object.

## Mistakes to Avoid
- God facade that knows everything — split by use case (`BillingFacade`, `OnboardingFacade`).
- Facade that becomes the only path and hides useful subsystem features without documentation.
