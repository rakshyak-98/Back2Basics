JavaScript library helps manage immutable data structures.
- It allows you to work with immutable data by using mutable syntax while ensuring that the original data remains unchanged.

> [!INFO] Immer uses drafts to represent temporary objects that you can mutate directly. Once the mutation is complete, Immer returns a new immutable state.
- Immer uses structural sharing to ensure that only modified parts of the data are updated, making it highly efficient compared to copying large data structures.