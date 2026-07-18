`e.dataTransfer` -> available on all-related events. The data carrier object that lives during the entire drag gesture.
- temporary storage that carries data during the whole drag operation.

|Property / Method|When you usually use it|Typical example|Read / Write?|
|---|---|---|---|
|`e.dataTransfer.setData()`|`dragstart`|`setData("text/plain", id)`|write|
|`e.dataTransfer.getData()`|`drop`|`getData("text/plain")` → read the ID|read|
|`e.dataTransfer.effectAllowed`|`dragstart`|`"move"`, `"copy"`, `"link"`, `"copyMove"` etc|read/write|
|`e.dataTransfer.dropEffect`|`dragover` (mainly)|controls cursor (copy/move/forbidden)|read/write|
|`e.dataTransfer.types`|`dragover` / `drop`|list of available formats (array-like)|read only|
|`e.dataTransfer.files`|`drop` (file drag)|dragged files from desktop|read only|
|`e.dataTransfer.items`|advanced / multi-format use cases|`DataTransferItemList` (modern way)|read only|


```js
// What you write in 95% of simple apps
function handleDragStart(e) {
  e.dataTransfer.setData("text/plain", "item-123");   // or JSON.stringify(obj)
}

function handleDragOver(e) {
  e.preventDefault();           // ← mandatory to allow drop!
  e.dataTransfer.dropEffect = "move";   // visual feedback
}

function handleDrop(e) {
  e.preventDefault();
  const data = e.dataTransfer.getData("text/plain");
  // → "item-123"
  // now move DOM element, update state, etc.
}
```