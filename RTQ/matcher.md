[[RTQ Concepts]]

# RTK Query matchers

> `addMatcher` on a slice reacts to RTK Query lifecycle actions — merge remote payloads into local UI state when hooks alone are not enough.





## Interview Relevance
Interviewers check whether you split matchers only when order/state dependency matters — not cargo-cult multiple empty matchers.

## Sources
- [Redux Toolkit — Matching utilities](https://redux-toolkit.js.org/api/matching-utilities) — deep-dive
- [RTK Query — Customizing queries](https://redux-toolkit.js.org/rtk-query/usage/customizing-queries) — overview

## Key Concepts
- **Matchers run sequentially** for the same action.
- **Split only if dependent:** second matcher reads state written by the first.
- **Prefer endpoint handlers / tags** when you only need cache updates.
- **`matchFulfilled` / `matchPending` / `matchRejected`:** generated action matchers from endpoints.

## Technical Details
Dependent split (makes sense):

```js
.addMatcher(api.endpoints.getHotelDetailsWebBooking.matchFulfilled, (state, action) => {
  state.locations = action.payload?.data;
})
.addMatcher(api.endpoints.getHotelDetailsWebBooking.matchFulfilled, (state, action) => {
  state.selectedHotel = state.locations?.[0];
})
```

If both only read `action.payload`, combine into one matcher — identical behavior, less noise.

## Real-World Applications
Keep “selected entity” in a UI slice while RTK Query owns the server cache.

**Example:** Two matchers both set fields from `action.payload` — merge them; sequential split adds no value.

## Pros/Cons or Trade-offs
- **Pro:** Escape hatch when UI state must derive from query results.
- **Con:** Easy to duplicate cache already in RTK Query.

## Comparison
- vs `extraReducers` builder with `addCase`: matchers are for shared patterns across many actions.
- vs component `useEffect`: matchers keep derivation in the store.

## Mistakes to Avoid
- Multiple matchers on the same event with no dependency between them.
- Re-storing the entire server response in a parallel slice without a reason.
- Ignoring rejected matchers for error UX.
