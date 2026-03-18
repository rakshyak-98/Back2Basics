In Redux Toolkit, multiple matchers for the same event **do run sequentially**, but splitting them into separate matchers here provides **no benefit** because:

1. Both matchers react to the **same event**
2. They don't depend on each other's result
3. There's no side effect or ordering logic between them

The sequential execution only matters when the **second matcher depends on state changed by the first**, for example:


```js
// This makes sense split — second reads what first wrote
.addMatcher(event, (state, action) => {
  state.locations = action.payload?.data;        // sets locations
})
.addMatcher(event, (state, action) => {
  state.selectedHotel = state.locations?.[0];    // reads locations ← depends on above
})
```

But in your code both matchers read directly from `action.payload`, not from each other, so **combining them is identical in behavior:**

```js
.addMatcher(
  api.endpoints.getHotelDetailsWebBooking.matchFulfilled,
  (state, action) => {
    state.locations = action.payload?.data;
    state.selectedHotel = action.payload?.data[0]; // same source
  }
)
```

So it's safe to merge — it was likely just written that way out of habit or copy-paste, not intentional sequencing.