- every DOM element is represented in WebDriver by a unique identifying reference, known as a **web element**.
 - the **web element** reference is a UUID used to execute commands targeting specific elements, such as getting an element's tag name and retrieving a property off an element.

> [!NOTE] When an element is no longer attached to the DOM, i.e. it has been removed from the document or the document has changed, it is said to be *stale*.
> 
- Staleness occurs for example when you have a web element reference and the document it was retrieved from navigates.
- upon navigation, all web element references to the previous document will be discarded along with the document. This will cause any subsequent interaction with the **web element** to fail with the stale element reference error.