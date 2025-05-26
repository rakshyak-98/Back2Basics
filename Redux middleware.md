## Add multiple mather
```js
import { isAnyOf } from '@reduxjs/toolkit';
import { apiCall1, apiCall2, apiCall3 } from './api';

const customMiddleware = (store) => (next) => (action) => {
  // your logic
  return next(action);
};

// inside middleware registration, use .addMatcher
const myMiddleware = (builder) => {
  builder
    .addMatcher(
      isAnyOf(apiCall1.pending, apiCall2.fulfilled, apiCall3.rejected),
      (state, action) => {
        // handle any of these actions
      }
    )
    .addMatcher(
      (action) => action.type.endsWith('/rejected'),
      (state, action) => {
        // generic error handler
      }
    );
};

```
> [!INFO]
> in redux toolkit you can add multiple matchers in a middleware using `isAnyOf` or by chaining `.addMatcher()` calls.
