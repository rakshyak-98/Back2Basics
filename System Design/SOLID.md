### Program to an Interface, not an Implementation

> Program to an interface, not an implementation. Depend on abstractions, not on concrete classes

A `Cat` that can eat any food is more flexible than one that can eat just "sausages". You still feed the first cat with sausages because they are a subset of of "any food"; however, you can extend that cat's menu with any other food.

> [!NOTE]
> - to make two classes collaborate, you can start by making one of them dependent on the other.

#### Setup collaboration between objects

- Determine what exactly one object needs from the other: Which methods does it execute?
- Describe these methods in a new interface or abstract class.
- Make the class that is a dependency implement this interface.
- Now make the second class dependent on this interface rather than on the concrete class. You still can make it work with objects of the original class, but the connection is now much more flexible.
### Favor Composition Over Inheritance

- A subclass can't reduce the interface of the super-class. You have to implement all abstract methods of the parent class even if you won't be using them.
- When overriding methods you need to make sure that the new behavior is compatible with the base one. It's important because object of the subclass may be passed by to any code that expects objects of the super-class and you don't want that code to break.
- Inheritance breaks encapsulation of the super-class because the internal details of the parent class become available to the subclass. There might be an opposite situation when a programmer makes a superclass aware of some details of subclasses for the sake of making future extension easier.
- subclass are tightly coupled to superclasses. Any change in a superclass may break the functionality of subclasses.
- Trying to reuse code through inheritance can lead to creating parallel inheritance hierarchies. Inheritance usually takes place in a single dimension. But whenever there are two or more dimensions, you have to create lots of class combinations, bloating the class hierarchy to a ridiculous size.

### Single responsibility
- each class should have only one responsibility and one reason to change.
- the SRP says to separate the code that different actors depend on.
- aims to separate behaviors so that if bugs arise as a result of your change, it won't affect other unrelated behaviors.
### Open close
- open for extension and close of modification
- we should be able to change the class as per business requirements without breaking the code.
- abstraction is used to implement open to extension and closed to modification.
- abstraction feature tells the compiler that class is a blueprint and incomplete class (do not have body of function).
- extend a class's behavior without changing the existing behavior of that class. This is to avoid causing bugs wherever the class is being used.
### Liskov substitution
### Interface segregation
### Dependency inversion
