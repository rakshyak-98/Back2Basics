# Store Architecture Guide

> Reference document for maintaining and extending the Redux store after refactoring.
> Last updated: March 2026

---

## Table of Contents

1. [Folder Structure](#folder-structure)
2. [Core Concepts](#core-concepts)
3. [Slice Rules](#slice-rules)
4. [Middleware Rules](#middleware-rules)
5. [API Layer Rules](#api-layer-rules)
6. [Storage Abstraction](#storage-abstraction)
7. [Adding a New Feature](#adding-a-new-feature)
8. [Removing a Feature](#removing-a-feature)
9. [Dependency Map](#dependency-map)
10. [Common Pitfalls](#common-pitfalls)
11. [Refactoring History](#refactoring-history)

---

## Folder Structure

```
src/
  store/
    index.js                        # configureStore only — imports reducers and middlewares
    rootReducer.js                  # combines all feature reducers
    middleware/
      index.js                      # combines and exports all middlewares
      storageMiddleware.js          # sessionStorage / localStorage sync listeners
      apiMiddleware.js              # API response side effect listeners
      stateMiddleware.js            # cross-slice state sync listeners

  features/
    search/
      searchQuerySlice.js           # slice + actions + initial state
      searchQuerySelectors.js       # all selectors for this feature
    guestRoom/
      guestRoomSlice.js
      guestRoomSelectors.js
    roomList/
      roomListSlice.js
      roomListSelectors.js
    reservation/
      reservationSlice.js
      reservationSelectors.js
    pricing/
      pricingSlice.js
      pricingSelectors.js
    auth/
      authSlice.js
      authSelectors.js
    hotelDetails/
      hotelDetailsSlice.js
      hotelDetailsSelectors.js

  api/
    apiSlice.js                     # createApi + baseQuery
    endpoints/
      booking.js                    # getDataForWebBooking, addReservationFromWeb
      hotel.js                      # getHotelDetailsWebBooking
      auth.js                       # webLogin
      reservation.js                # getReservationJsonLikeEzeeWebBooking, getFinalReservationDetailsWeb

  utils/
    formatDate.js                   # moment date formatting helpers
    browserStorageKeys.js           # all storage key constants
    storage.js                      # sessionStorage / localStorage wrapper
```

---

## Core Concepts

### Three Middleware Responsibilities

| Middleware File | Responsibility | Example |
|---|---|---|
| `storageMiddleware.js` | Sync state → sessionStorage/localStorage | Save `roomChooises` on `insertRoomOptions` |
| `apiMiddleware.js` | Handle API response side effects | Save `orderID` after `addReservationFromWeb` |
| `stateMiddleware.js` | Sync state across slices | Update `quantity` in `searchQuery` after `insertRoomOptions` |

> **Rule:** If you are unsure which middleware file to put a listener in, ask: is this saving to storage? handling an API response? or syncing two slices? That answer tells you the file.

### Listener API vs RTK Query API

Inside a listener `effect`, the second parameter is the **listener API** — not the RTK Query `api`.

```js
// ✅ correct — reference the imported `api` (createApi instance) directly
import { api } from "@/api/apiSlice";

stateMiddleware.startListening({
  actionCreator: someSlice.actions.someAction,
  effect: (action, listenerApi) => {  // listenerApi ≠ RTK Query api
    listenerApi.dispatch(api.endpoints.someEndpoint.initiate(payload));
  }
});
```

---

## Slice Rules

Every slice must follow these rules without exception.

### Rule 1 — Export initial state

```js
// ✅ always export so middleware, tests, and reset logic can reference it
export const guestRoomInitialState = {
  currentRoom: { id: 1, name: "Room 1", adults: 1, children: 0 },
  roomChooises: [{ id: 1, name: "Room 1", isSelected: true, adults: 1, children: 0 }],
  roomPicked: {}
};

const guestRoomSlice = createSlice({
  name: "guestRoom",
  initialState: guestRoomInitialState,
  ...
});
```

### Rule 2 — A slice owns only its own state

```js
// ❌ never update another slice's state inside a reducer
// cross-slice updates belong in stateMiddleware.js

// ✅ keep reducers focused on their own state only
```

### Rule 3 — All state fields declared in initialState

```js
// ❌ adding state fields only in reducers causes undefined on first render
reducers: {
  setPriceSummary: (state, action) => {
    state.priceSummary = action.payload; // ❌ not in initialState
  }
}

// ✅ always declare in initialState first
initialState: {
  OverallTotal: {},
  BookingTran: [],
  finalReservationDetails: [],
  priceSummary: {}  // ✅ declared
}
```

### Rule 4 — Export actions and reducer separately

```js
export const guestRoomActions = guestRoomSlice.actions;
export default guestRoomSlice.reducer;
```

### Rule 5 — Selectors live in their own file

```js
// features/guestRoom/guestRoomSelectors.js
export const selectCurrentRoom = (state) => state.guestRoom.currentRoom;
export const selectRoomChoices = (state) => state.guestRoom.roomChooises;
export const selectRoomPicked = (state) => state.guestRoom.roomPicked;
```

> **Why:** If state shape changes, fix selectors in one file — not across every component.

---

## Middleware Rules

### Rule 1 — Use `isAnyOf` for identical effects on multiple actions

```js
import { isAnyOf } from "@reduxjs/toolkit";

// ❌ two listeners with identical effects
storageMiddleware.startListening({ actionCreator: guestRoom.actions.updateAdults, effect: syncRoomChoices });
storageMiddleware.startListening({ actionCreator: guestRoom.actions.updateChildren, effect: syncRoomChoices });

// ✅ one listener with isAnyOf
storageMiddleware.startListening({
  matcher: isAnyOf(guestRoom.actions.updateAdults, guestRoom.actions.updateChildren),
  effect: (_action, api) => {
    const state = api.getState();
    storage.session.set(sessionStorageKeys.roomChooises, state.guestRoom.roomChooises);
  }
});
```

### Rule 2 — Extract shared listener logic into helpers

```js
// ✅ shared logic extracted — used by both selectRoom and pickRoom listeners
const dispatchWebBooking = (listenerApi) => {
  const { searchQuery, guestRoom } = listenerApi.getState();
  const { currentRoom } = guestRoom;
  listenerApi.dispatch(
    api.endpoints.getDataForWebBooking.initiate({
      ...searchQuery,
      adults: currentRoom?.adults,
      children: currentRoom?.children
    })
  );
};
```

### Rule 3 — Never duplicate listeners for the same matcher

```js
// ❌ two separate listeners for the same matchFulfilled
apiMiddleware.startListening({ matcher: api.endpoints.addReservationFromWeb.matchFulfilled, effect: saveOrderID });
apiMiddleware.startListening({ matcher: api.endpoints.addReservationFromWeb.matchFulfilled, effect: saveConfirmation });

// ✅ merge into one listener
apiMiddleware.startListening({
  matcher: api.endpoints.addReservationFromWeb.matchFulfilled,
  effect: (action, api) => {
    const { order_id } = action.payload;
    storage.session.set(sessionStorageKeys.orderID, order_id);
    storage.session.set(sessionStorageKeys.orderDetails, action.payload);
    storage.session.set(sessionStorageKeys.reservationConfirmation, action.payload);
  }
});
```

### Rule 4 — Never use `api.getState()` if state is not used

```js
// ❌ unnecessary getState call
effect: (action, api) => {
  const state = api.getState(); // never used
  sessionStorage.setItem(...);
}

// ✅ remove unused state
effect: (action) => {
  sessionStorage.setItem(...);
}
```

---

## API Layer Rules

### Endpoint files are grouped by domain

```js
// api/endpoints/booking.js
export const bookingEndpoints = (builder) => ({
  getDataForWebBooking: builder.mutation({ ... }),
  addReservationFromWeb: builder.mutation({ ... }),
});

// api/apiSlice.js
import { bookingEndpoints } from "./endpoints/booking";
import { hotelEndpoints } from "./endpoints/hotel";

export const api = createApi({
  reducerPath: "api",
  baseQuery: ...,
  endpoints: (builder) => ({
    ...bookingEndpoints(builder),
    ...hotelEndpoints(builder),
  })
});
```

### Base query delay is dev-only

```js
// ✅ never ship artificial delays to production
if (process.env.NODE_ENV === "development") {
  await new Promise((resolve) => setTimeout(resolve, 1000));
}
```

### Use `.unwrap()` with `toast.promise`

```js
// ✅ .unwrap() converts RTK Query result to a standard Promise
toast.promise(
  getDataForWebBooking({ ... }).unwrap(),
  {
    loading: "Checking availability...",
    error: (err) => err?.data?.message || "Something went wrong. Please try again."
  }
);
```

---

## Storage Abstraction

All storage access goes through the `storage` utility — never call `sessionStorage` or `localStorage` directly.

```js
// utils/storage.js
const storage = {
  session: {
    get: (key) => JSON.parse(sessionStorage.getItem(key)),
    set: (key, value) => sessionStorage.setItem(key, JSON.stringify(value)),
    remove: (key) => sessionStorage.removeItem(key),
    clear: (keys) => keys.forEach((key) => sessionStorage.removeItem(key))
  },
  local: {
    get: (key) => JSON.parse(localStorage.getItem(key)),
    set: (key, value) => localStorage.setItem(key, JSON.stringify(value)),
    remove: (key) => localStorage.removeItem(key)
  }
};

export default storage;
```

```js
// ✅ usage in middleware
import storage from "@/utils/storage";
import { sessionStorageKeys } from "@/utils/browserStorageKeys";

storage.session.set(sessionStorageKeys.roomChooises, state.guestRoom.roomChooises);
storage.session.get(sessionStorageKeys.roomPick);
storage.session.clear(["guestDetails", "roomSelection", "roomPick"]);
```

---

## Adding a New Feature

Follow this checklist in order. No existing files need to be modified.

```
□ 1. Create features/<featureName>/<featureName>Slice.js
       - Define and export initialState
       - Define reducers
       - Export actions and default reducer

□ 2. Create features/<featureName>/<featureName>Selectors.js
       - Export one selector per state field

□ 3. Add reducer to rootReducer.js
       import featureReducer from "@/features/featureName/featureNameSlice";
       featureName: featureReducer

□ 4. Add API endpoints to api/endpoints/<domain>.js if needed
       - Add to the relevant domain file (booking, hotel, auth, reservation)

□ 5. Add storage listeners to middleware/storageMiddleware.js if needed
       - Only for persisting state to sessionStorage/localStorage

□ 6. Add API response listeners to middleware/apiMiddleware.js if needed
       - Only for handling API response side effects

□ 7. Add cross-slice listeners to middleware/stateMiddleware.js if needed
       - Only for syncing state across multiple slices

□ 8. Export actions from store/index.js
       export { featureNameActions } from "@/features/featureName/featureNameSlice";
```

---

## Removing a Feature

```
□ 1. Delete features/<featureName>/ folder entirely
□ 2. Remove reducer from rootReducer.js
□ 3. Remove any listeners referencing this feature from middleware files
□ 4. Remove any API endpoints from api/endpoints/ if exclusively used by this feature
□ 5. Remove exports from store/index.js
□ 6. Search codebase for any remaining imports and remove them
```

---

## Dependency Map

Cross-slice dependencies — which slices react to which actions.

```
searchQuery  ←── guestRoom.updateAdults
searchQuery  ←── guestRoom.updateChildren
searchQuery  ←── guestRoom.pickRoom
searchQuery  ←── guestRoom.insertRoomOptions   (quantity sync)
searchQuery  ←── guestRoom.removeRoom          (quantity sync)

roomList     ←── searchQuery.setBookingQuery   (clears roomTypes)
roomList     ←── api.getDataForWebBooking      (pending / fulfilled / rejected)

reservation  ←── searchQuery.setBookingQuery   (merges payload)
reservation  ←── guestRoom.pickRoom            (updates guestDetails)
reservation  ←── guestRoom.insertRoomOptions   (updates quantity)
reservation  ←── guestRoom.removeRoom          (removes guestDetails + quantity)
reservation  ←── api.addReservationFromWeb     (saves reservationIDs)

pricing      ←── api.getReservationJsonLikeEzeeWebBooking  (sets BookingTran + OverallTotal)

api          ←── guestRoom.selectRoom          (triggers getDataForWebBooking)
api          ←── guestRoom.pickRoom            (triggers getDataForWebBooking)
```

> **When adding a new cross-slice dependency, update this map.**

---

## Common Pitfalls

### 1. Stale closure in `useCallback`

```js
// ❌ missing deps causes stale values
const handleSomething = useCallback(() => {
  doSomething(currentRoom); // stale if currentRoom not in deps
}, [dispatch]); // ❌ missing currentRoom

// ✅ include all used values
}, [dispatch, currentRoom]);
```

### 2. Resetting state but saving old value to storage

```js
// ❌ roomChooises here is the pre-reset value from closure
dispatch(guestRoomActions.reset());
storage.session.set(sessionStorageKeys.roomChooises, roomChooises); // ❌ stale

// ✅ use a storageMiddleware listener for guestRoom.reset instead
storageMiddleware.startListening({
  actionCreator: guestRoom.actions.reset,
  effect: (_action, api) => {
    const state = api.getState(); // ✅ always post-reset state
    storage.session.set(sessionStorageKeys.roomChooises, state.guestRoom.roomChooises);
  }
});
```

### 3. `react-multi-date-picker` DateObject timezone issue

```js
// ❌ .toDate() causes timezone shift in IST (+05:30)
const formatted = moment(date.toDate()).format("YYYY-MM-DD");

// ✅ use DateObject.format() directly — no timezone conversion
const formatted = date.format("YYYY-MM-DD");
```

### 4. Double formatting dates

```js
// ❌ arrival.format() already returns "YYYY-MM-DD" string
// passing it to formatDate() wraps it in new Date() again
arrivalDate: formatDate(arrival.format("YYYY-MM-DD")), // ❌

// ✅ use directly
arrivalDate: arrival.format("YYYY-MM-DD"), // ✅
```

### 5. Using `api.endpoints` inside listener effect

```js
// ❌ api here is the listener API, not RTK Query api
effect: (action, api) => {
  api.endpoints.getDataForWebBooking.initiate(...) // ❌ undefined
}

// ✅ import the RTK Query api directly and use a different param name
import { api } from "@/api/apiSlice";

effect: (action, listenerApi) => {
  listenerApi.dispatch(api.endpoints.getDataForWebBooking.initiate(...)) // ✅
}
```

---

## Refactoring History

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Safe fixes — unused vars, missing initialState fields, dev delay gate | ✅ Done |
| Phase 2 | Deduplication — merged duplicate matchers and listeners | ✅ Done |
| Phase 3 | Logic extraction — shared helpers for repeated listener logic | ✅ Done |
| Phase 4 | Behavioral — narrowed roomList clearing to date/hotel changes only | ✅ Done |
| Phase 5 | Folder restructure — feature-first folder structure | ✅ Done |
| Phase 6 | Slice design rules — selectors, exported initialState, separated actions | ✅ Done |
| Phase 7 | Middleware split — storageMiddleware, apiMiddleware, stateMiddleware | ✅ Done |
| Phase 8 | API layer split — endpoints grouped by domain | ✅ Done |
| Phase 9 | Storage abstraction — storage utility wrapper | ✅ Done |
