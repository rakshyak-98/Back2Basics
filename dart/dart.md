[[dart]]

# dart

> dart — factory — Unlike a normal constructor, a factory constructor can return an existing instance or even a subclass. In this context, it's used to return a

---

## Mental model

**Say it in one breath:** dart — factory — Unlike a normal constructor, a factory constructor can return an existing instance or even a subclass. In this context, it's used to return a

`factory ApiRoomDate.fromJson(...)`
- Factory -> Unlike a normal constructor, a `factory` constructor can return an existing instance or even a subclass. In this context, it's used to return a fully populated `ApiRoomData` object after processing the JSON.
- Map<String, dynamic>  -> This represents the structure of a standard JSON object (keys are Strings, values can by anything)


---

## Related

[[dart]]
