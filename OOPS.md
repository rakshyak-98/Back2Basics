##### Constructors
- special type of member function.
- initialize an object.
- block of memory created when the constructor of a function is invoked.

##### default constructor
- no return type
- no input argument.

### UML diagram
Unified Modeling Language
- DIPD - **Design Implementations Process Design**
	D - consists of classes, interfaces
	implementations - 
	Process -
	Design -

- `+` public
- `-` private
- `#` protacted 

| ClassName | Employee |
| ----------- | ----------- |
| Class attribute | Name GroupId |
| Class operations | `getAdd()`, `getSet()` |

- visual the system
- documentation
1. timing
2. relationships
3. diagrams 

#### things
| Structural | Behavioral | Grouping |
| ------------- | ---------- | ---------- |
| static part of model | Dynamic part of UML model | Grouping elements of UML model together |
| | passing message from one class to another | gathering structure and behavioral thing |
- class, interface 
- interaction 
- package

#### Relationships
1. dependency: change in one element affects the other  ---->
2. association : set of links connecting other. <--- ----->
3. genarilized : connect spaclized element with general element. ====>

#### Realization
- a relationship in which two elements are connected where one element is responsible which is not implemented yet, and another element implements it.

### Object diagram
- is a instance of a class diagram.
- represent instance of class diagram.
- static view of system at moment at a particular moment.

### State diagram
- also known as behavioral diagram.
- moment in the life-cycle of an object.
- event : trigger where it jumps from one stat to another.
- Final state : flow stop here.
- Decision box : what to do next (diverge path).

### Activity
- dynamic aspects of a system. 
- Flow of the system from one activity to another.
- activity - to describe the dynamic aspects of a system.
- flow of system from one activity to another activity.
- represent in rounded rectangle rounded cornors.

#### User cases
- Modelling workflow.
- Modelling business requirements.
- high level understanding of system.
- business requirements.

### Sequence diagram (Behavioral)
- flow of messages in a system (also called as event diagram). 
- represent in different formats
	- lifeline (no overlap) : runs from top to bottom and they signify the presence of object.
	- Actor : role played by an entity that interacts with subject.
	- Activation bar : thin rectangle on the lifeline time period in which an operation has been performed.
	- messages : it depicts the interaction between objects and is represented by an arrow.

### messages
- synchronous - waits for the reply of a receive so as to carry forward the interaction.
- Asynchronous - It doesn't wait for the reply to come.
- Return - flow from receive to the caller.
- self - message of same lifeline has been invoked.
- start - it describes the target has been instantiated.
- destroy - depicts a request to destroy lifecycle of a target.

#### pros of a Sequence diagram
- explores real time application.
- depicts message flow between object.
- easy to generate and maintain.