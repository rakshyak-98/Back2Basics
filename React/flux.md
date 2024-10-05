- an application architecture used in React for managing data flow. It promotes unidirectional data flow, making it easier to understand and maintain the state of an application.
## Components
- Actions: Objects that contain the data to be sent to the store. Actions are created to initiate changes in application state.
- Dispatcher: A central hub that manages the flow of data and facilitates communication between actions and stores. It receives actions and dispatches them to the appropriate store.
- Stores: Containers for application state and logic. They listen for actions dispatched by the dispatcher and update their state accordingly. They also emit change events to notify views.
- Views: React components that display data from the stores. They subscribe to store changes and re-render when the data changes.