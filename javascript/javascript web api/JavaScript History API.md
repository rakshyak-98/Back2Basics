No, the browser API does not store the state of all the visited paths by default.
- Different browser components manage navigation history in specific ways:

### Browser history API (`window.history`)
- Stores: a stack of visited URLs within the session (limited to same-origin policies).
- Access: you can navigate backward (`history.back()`), forward (`history.forward`), or move withing the stack (`history.go(n)`).

> [!INFO] doesn't persist state beyond the sesison.

### IndexedDB / Cache API
- Stores: Persistent structured data across sessions.
- User Case: Web apps that need offline support.

```js

history.pushState({page: 1}, "Page 1", "/page1")

history.replaceState({ page: 2}, "Page 2", "/page2")

window.addEventListener("popstate", (event) => {
	console.log("Navigated to state:", event.state)
})
```