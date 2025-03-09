- Defines a family of algorithms, encapsulates each one, and makes them interchangeable.
- Behavior is selected on runtime.
- take the parts the vary and encapsulate them, so that later you can alter or extend the parts that vary without affecting those that don't.
- behavior live in different class (a class that implements a particular behavior interface), include behavior setter methods in the class so that we can, change the behavior at runtime.

> [!INFO] **Separation of Concerns** and the **Strategy Pattern**I
> - if a part of the code frequently changes with new requirements, it indicates a behavior that should be **extracted** and **separated** from the stable parts of the system. This promotes flexibility, maintainability, and adherence to principles like **Separation of Concerns** and the **Strategy Pattern**.

### Code smell
- created one super class from which all other sub class inherit. This happens because of using _inheritance for the purpose of reuse_
	- needed to override inherited methods in subclass.
- using inheritance to provide behavior.
- whenever you need to modify a behavior, changes are required to be made in all the subclasses where that behavior is defined.

### Usage
- Payment processing with different payment gateway like PayPal, Stripe, or Credit card, all implementing a common `PaymentProcessor` interface.

### Separating what changes from what stays the same
- To separate behaviors from the class, pull methods out of the class and create a new set of classes to represent each behavior.

> [!INFO] Implementation details
> - won't need to know any of the implementation details for their own behaviors.
> - program to an interface means program to a supertype. The point is to exploit polymorphism by programming to a supertype so that the actual runtime object isn't locked into the code.