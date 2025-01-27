## Abstraction and Implementation Hierarchies
In software design, separate abstraction and implementation hierarchies refer to 
- decoupling the high level logic (abstraction) from its underlying details (implementation).
This separation allows both the abstraction and its implementation to evolve independently without tightly coupling them.

#### Abstraction
- represents the high-level functionality or concept.
- does not know the implementation details.
- typically defines what need to be done (e.g., an interface or abstract class).

#### Implementation
- contains the specific details of how something is done.
- implements the behavior defined by the abstraction.

##### Why separate them?
- you can extend either abstraction or implementation without affecting the other.
- adding new features or implementation is easier.
- implementations can be reused with different abstraction.