[[JRE]] **Provides** the environment required to run java applications, conceptually JVM + runtime libraries.
[[JDK]] Used to develop java applications. It provides tools such as `javac` (compiler).
[[JVM]] Java Virtual Machine. **Java one each machine** Executes java bytecode `.class` files

"JDK is used for developing Java application and provides development tools such as the `javac` compiler. JRE provides the runtime environment needed to run Java applications, including the JVM and runtime liberaries. JVM executes java bytecode. Java is platform-independent because the source code is compiled into platform-independent bytecode, and the same bytecode can be executed on different operating systems by their respective JVM."

"Java is a platform-independent because Java source code is compiled into platform independent bytecode. The bytecode is executed by a platform-specific JVM, so the same `.class` file can run on different operating system."

## OOP Fundamentals Class Vs Object

A **class** is a blueprint that defines the **state of behavior** of objects.
An **object** is an actual instance created from that class.
The class defines what an object of the class **can contain and do.**

**Encapsulation:** Bundling data and methods together and controlling access to the data, **how it is accessed or modified** using the access modifiers `private` or `public` properties/methods.
**Abstraction:** Hiding implementation details and exposing only the essential functionality.
[[Java/Inheritance]]: Inheritance allows a child class to acquire the properties and behaviors of a parent class. In java, class inheritance is achieved using `extends`, mainly for code reuse and establishing as is-a relationship Allowing a class to acquire properties and behavior from another class using `extends`.
[[Java/Polymorphism]] The same **interface/method call** can produce different behavior depending on the object or parameters involved. Commonly discussed as **method overloading (Compile-time polymorphism)** and **method overriding (runtime polymorphism).**

**Method overloading:** Same method name, but **different parameter lists.**
**Method overriding:** A child class provides its own implementation of a method inherited from the parent
