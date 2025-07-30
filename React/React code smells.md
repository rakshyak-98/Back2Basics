1. A single component that handles too much logic, rendering and state management.
	- Use custom hooks or utility functions to extract complex logic.
	
2. Passing props through multiple layers of component just to get them to a deeply nested child
	- User react context state management library
	- consider restructuring components to reduce the depth of the component tree.

3. Using state for data that doesn't need to be reactive or could be derived from props.
	- user derived state or memoization (`useMemo`) for computed values.
	- avoid duplicating props in state unless absolutely necessary.