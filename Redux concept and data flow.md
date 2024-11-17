components are located in different parts of the application. Sometimes this can be solved by "lifting state up" to parent components, but that doesn't always help.
- one way to solve this is to extract the share state from the components, and put it into a centralized location outside the component tree.

> A basic idea behind Redux: a single centralized place to contain the global state in your application, and specific patterns to follow when updating that state to make the code predictable.

