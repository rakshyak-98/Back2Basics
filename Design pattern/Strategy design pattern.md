- Defines a family of algorithms, encapsulates each one, and makes them interchangeable.
- Behavior is selected on runtime.

> [!INFO] **Separation of Concerns** and the **Strategy Pattern**I
> - if a part of the code frequently changes with new requirements, it indicates a behavior that should be **extracted** and **separated** from the stable parts of the system. This promotes flexibility, maintainability, and adherence to principles like **Separation of Concerns** and the **Strategy Pattern**.

### Code smell
- created one super class from which all other sub class inherit. This happens because of using _inheritance for the purpose of reuse_
	- needed to override inherited methods in subclass.
- using inheritance to provide behavior.
- whenever you need to modify a behavior, changes are required to be made in all the subclasses where that behavior is defined.

### Usage
- Payment processing with different payment gateway like PayPal, Stripe, or Credit card, all implementing a common `PaymentProcessor` interface.