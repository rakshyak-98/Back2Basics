instead of shipping a feature directly to all users, you wrap it behind a conditional check that can be toggled on or off remotely.

```js
if(featureFlags.isEnabled('new-checkout')){
	showNewCheckout();
} else {
	showOldCheckout();
}

```
- The flag's value is controlled externally through a dashboard, API, or configuration service, not hardcoded in source code.