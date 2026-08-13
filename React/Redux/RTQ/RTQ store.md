[[react hooks]] [[React State management]] [[React Architecture]] [[RTQ Toolkit]] [[RTQ tags]] [[redux store architecture]]

# RTQ store

> RTQ store shapes how React applications compose UI, state, and side effects in production.

## What this is

Redux centralizes application state in a single store updated through dispatched actions and pure reducers. Redux Toolkit is the recommended integration path: `configureStore`, `createSlice`, and `createAsyncThunk` replace hand-written action types and boilerplate ([Redux Toolkit overview](https://redux.js.org/redux-toolkit/overview)).

## What breaks first

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Invalid hook call warning | Hook outside component or duplicate React copies | Call hooks only from components/custom hooks; dedupe `react` in bundle |
| Hydration mismatch | Server HTML differs from client render | Fix conditional rendering; avoid `Date.now()` in SSR output |
| State updates but UI stale | Mutation without setter | Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references |

## Recall

What breaks first in production if `RTQ store` is misused — bundle size, stale UI, or hydration errors?

## Related

[[react hooks]] [[React State management]] [[React Architecture]] [[RTQ Toolkit]] [[RTQ tags]] [[redux store architecture]]
