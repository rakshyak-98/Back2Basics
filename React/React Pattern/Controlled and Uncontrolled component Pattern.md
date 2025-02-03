## When to use:
- Controlled: When you need to manage the form state or respond to changes immediately (form validation, conditional rendering)
- Uncontrolled: When you don't need to track every input change, reducing overhead, especially for forms that don't require much interaction.

- Controlled Components: Components that are controlled by React state.
- Uncontrolled Components: Components that maintain their own internal state.

This pattern helps manage form element, input validation, and UI integrations, providing flexibility for managing state externally or letting the component handle its own state.

### Controlled Component
- controlled via react state.
- the component value is always synchronized with the state.

```js
import { useState } from 'react';

const ControlledInput = () => {
  const [value, setValue] = useState('');

  const handleChange = (e) => {
    setValue(e.target.value);
  };

  return (
    <div>
      <label>Enter your name: </label>
      <input
        type="text"
        value={value}
        onChange={handleChange}
      />
      <p>Your input: {value}</p>
    </div>
  );
};
export default ControlledInput;
```

#### Uncontrolled Component
- the input manages its own state internally, and React doesn't directly control it.

```jsx
import { useRef } from 'react';

const UncontrolledInput = () => {
  const inputRef = useRef();

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Input value: ${inputRef.current.value}`);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Enter your name: </label>
      <input type="text" ref={inputRef} />
      <button type="submit">Submit</button>
    </form>
  );
};

export default UncontrolledInput;
```
