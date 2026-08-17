[[RTQ Concepts]]

# RTK Query matchers

> `addMatcher` on a slice reacts to RTK Query lifecycle actions — merge remote payloads into local UI state when hooks alone are not enough.

```txt
        RTK Query matchers ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers check whether you split matchers only when order/state dependenc…

## Sources
- [Redux Toolkit — Matching utilities](https://redux-toolkit.js.org/api/matching-utilities) — deep-dive
- [RTK Query — Customizing queries](https://redux-toolkit.js.org/rtk-query/usage/customizing-queries) — overview

## Key Concepts
- **Matchers run sequentially:** for the same action.
- **Split only if dependent:** second matcher reads state written by the first.
- **Prefer endpoint handlers / tags:** when you only need cache updates.
- **`matchFulfilled` / `matchPending` / `matchRejected`:** generated action matchers from endpoints.

## Technical Details
- Dependent split (makes sense):

```js
.addMatcher(api.endpoints.getHotelDetailsWebBooking.matchFulfilled, (state, action) => {
  state.locations = action.payload?.data;
})
.addMatcher(api.endpoints.getHotelDetailsWebBooking.matchFulfilled, (state, action) => {
  state.selectedHotel = state.locations?.[0];
})
```

- If both only read `action.payload`, combine into one matcher

## Mistakes to Avoid
- **Mistake:** Multiple matchers on the same event with no dependency between t…
- **Mistake:** Re-storing the entire server response in a parallel slice withou…
- **Mistake:** Ignoring rejected matchers for error UX

## Pros/Cons or Trade-offs
- **Pro:** Escape hatch when UI state must derive from query results.
- **Con:** Easy to duplicate cache already in RTK Query.

## Comparison
- vs `extraReducers` builder with `addCase`: matchers are for shared patterns across many actions.
- vs component `useEffect`: matchers keep derivation in the store.


### Use cases
- Keep “selected entity” in a UI slice while RTK Query owns the server cache.

- **Example:** Two matchers both set fields from `action.payload`
