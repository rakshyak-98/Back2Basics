- General Responsibility Assignment Software Principle
- who does what. Which class or object is responsible for what action or role.
1. Creator : who instantiates what. Object B has responsibility to create A.
2. Information expert
3. Low coupling : how strongly one element is connected to others. Helps to support lower dependency between classes. Change in one class having a lower impact on other.
4. Controller
5. High Cohesion 
6. Indirection
7. Polymorphism
8. Protected variable 
9. Pure fabrication
##### Benefits
- define blueprint of objects class with methods implementing there responsibilities.
- identify the objects and responsibilities from person domain, and also identify how objects interact with each other.
##### Example
- whenever the book is added to the library a new Book instance is created.
- Assign a responsibility, so that coupling remains low
	- get video -> rent video -> get title -> videos
	- get video -> rent video -> get all video -> video store
- Low coupling
	- get video (title) -> rent video -> get all video -> video store -> get video (title) -> video