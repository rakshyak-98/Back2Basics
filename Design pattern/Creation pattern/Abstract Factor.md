lets you product families of related objects without specifying their concrete classes.
- in this you don't want to change existing code when adding new product.

> [!INFO] Abstract Factory pattern
> - suggests is to explicitly declare interfaces for each distinct product of the product family.
> - then you can make all variants of products follow those interfaces.
> - for each variant of a product family, we create a separate factory class based on the `AbstractFactory`

declare the Abstract Factory -> an interface with a list of creation methods for all products that are part of the product family

`createChair` `createSofa` `createCoffeeTable` -> these methods must return *abstract* product types represented by the interfaces we extracted previously
