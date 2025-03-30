1. Store Configuration (`configureStore`): Simplifies the store creation process by automatically setting up middleware like redux-thunk.
2. State Slices (`createSlice`): A slice is a single unit of Redux state, containing actions and a reducer in one place.
3. Asynchronous Actions (`createAsyncThunk`): Handles async logic, like API requests, with automatic action creation for pending, fulfilled, and rejected states.

> [!INFO] **Immer Integration:** Uses `Immer.js` for writing mutable code that gets converted to immutable updates internally.

> [!INFO] Many ESLint configs include the [no-param-reassign](https://eslint.org/docs/rules/no-param-reassign) rule, which may also warn about mutations to nested fields. 

> [!WARNING] In Immer powered reducers, no-param-reassign is not helpful
- To resolve this, you can tell the ESLint rule to ignore mutations and assignment to a parameter named `state` only in slice files:
```js
// @filename .eslintrc.js
module.exports = {
  // add to your ESLint config definition
  overrides: [
    {
      // feel free to replace with your preferred file pattern - eg. 'src/**/*Slice.ts'
      files: ['src/**/*.slice.ts'],
      // avoid state param assignment
      rules: { 'no-param-reassign': ['error', { props: false }] },
    },
  ],
}

```