> Replace direct object construction calls with calls to a special factory method.
- now you can override the factory method in subclass and change the class of products being created by the method. There's a slight limitation though: SubClasses may return different base class of interface. Also, the factory method in the base class should have its return type declare as the interface.
- despite its name, product creation is not the primary responsibility of the creator. Usually, the creator class already has some core business logic related to products.

lets you product families of related objects without specifying their concrete classes.
- in this you don't want to change existing code when adding new product.

> [!INFO] Abstract Factory pattern
> - suggests is to explicitly declare interfaces for each distinct product of the product family.
> - then you can make all variants of products follow those interfaces.
> - for each variant of a product family, we create a separate factory class based on the `AbstractFactory`

declare the Abstract Factory -> an interface with a list of creation methods for all products that are part of the product family

`createChair` `createSofa` `createCoffeeTable` -> these methods must return *abstract* product types represented by the interfaces we extracted previously
