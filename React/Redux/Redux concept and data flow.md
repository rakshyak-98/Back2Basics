[[Redux]] [[flux]] [[Redux toolkit]]

# Redux concept and data flow

> One store outside the tree — UI dispatches actions; reducers return next state; subscribers re-render.

## Mental model

**Say it in one breath:** Shared state lifts out of components into a store. Events become actions; pure reducers compute the next state; React-Redux connects reads/writes.

```txt
UI → dispatch(action) → reducer(s) → new state → useSelector → UI
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Single store** | One state tree | “Predictable; DevTools time travel.” |
| --- | --- | --- |
| **Action** | Plain event object | “`{ type, payload }`.” |
| **Reducer** | `(state, action) => next` | “Pure; no fetch inside.” |
| **Lifting state** | Parent holds shared data | “Redux when lift gets ugly.” |

## Standard config / commands

```ts
// RTK path (preferred)
const counter = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: { incremented(s) { s.value++ } },
})
const store = configureStore({ reducer: { counter: counter.reducer } })

function Counter() {
  const value = useSelector((s: RootState) => s.counter.value)
  const dispatch = useDispatch()
  return <button onClick={() => dispatch(counter.actions.incremented())}>{value}</button>
}
```

| Knob | Why it matters |

| Pure reducers | Time-travel + testability |
| --- | --- |
| Selectors | Limit re-renders |
| Middleware | Async, logging, persistence |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Prop drilling hell | Shared distant cousins | Introduce store/slice |
| State updates nowhere | Action type mismatch | Use slice action creators |
| Whole app re-renders | Selecting large objects | Narrow selector / `createSelector` |
| Side effects in reducer | Fetch inside reduce | Thunk / listener / RTK Query |

## Gotchas

> [!WARNING]
> **Redux doesn’t replace all local state** — forms and toggles often stay in the component.

> [!WARNING]
> **Mutating state outside Immer** — breaks purity; use `createSlice` drafts.

## When NOT to use

- **State used by one subtree** — Context or `useState`.
- **Server-driven UI only** — lean on RSC / URL / server cache.

## Related

[[flux]] [[Redux toolkit]] [[Redux/Redux createSlice]] [[Redux/redux store architecture]] [[React State management]]
