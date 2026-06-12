instead of shipping a feature directly to all users, you wrap it behind a conditional check that can be toggled on or off remotely.

```js
if(featureFlags.isEnabled('new-checkout')){
	showNewCheckout();
} else {
	showOldCheckout();
}

```
- The flag's value is controlled externally through a dashboard, API, or configuration service, not hardcoded in source code.

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Dashboard  │────>│  Flag Service    │────>│  Database   │
│  (Web UI)   │     │  (API Server)    │     │  (Postgres) │
└─────────────┘     └──────────────────┘     └─────────────┘
                              │
                       ┌──────┴──────┐
                       │             │
                  SSE/Polling    REST API
                       │             │
                 ┌─────v─────┐ ┌─────v─────┐
                 │ Client SDK│ │ Server SDK│
                 │ (Browser) │ │ (Node/Go) │
                 └─────┬─────┘ └─────┬─────┘
                       │             │
                 ┌─────v─────┐ ┌─────v─────┐
                 │ Your App  │ │ Your API  │
                 │ (Frontend)│ │ (Backend) │
                 └───────────┘ └───────────┘
```

## The Flag Service

An API that stores flag definitions, targeting rules, and percentage allocations. This is where the logic lives: "Enable `new-pricing` for 20% of users in a region who are on the Pro plan". The service evaluates rules and returns flag states for a given user context.

There are two fundamental approaches to flag evaluation

**Server side evaluation** ->  backend sends the user context to the flag service (or evaluates locally with a cached ruleset) and returns the computed flag values. The rules and logic never leave your server.

**Client side evaluation** -> browser SDK receives the evaluated flag values from the flag service (not the raw rules). The client knows what's enabled for the current user but doesn't see other user's configurations or your targeting logic.