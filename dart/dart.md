`factory ApiRoomDate.fromJson(...)`
- Factory -> Unlike a normal constructor, a `factory` constructor can return an existing instance or even a subclass. In this context, it's used to return a fully populated `ApiRoomData` object after processing the JSON.

- Map<String, dynamic>  -> This represents the structure of a standard JSON object (keys are Strings, values can by anything)


## Factory constructor
- is a specialized constructor that doesn't always create a new instance of its own class.
- while a generative constructor (the standard one) always creates a new object and initializes its fields, a factory constructor gives you more control over the instantiation process.