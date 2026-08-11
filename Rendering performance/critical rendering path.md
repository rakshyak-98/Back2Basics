[[Rendering performance]]

# critical rendering path

> critical rendering path — a crucial sequence of steps that web browsers follow to convert HTML, CSS and JavaScript into a visual representation on the screen.

---

## Mental model

**Say it in one breath:** critical rendering path — a crucial sequence of steps that web browsers follow to convert HTML, CSS and JavaScript into a visual representation on the screen.

- is a crucial sequence of steps that web browsers follow to convert HTML, CSS and JavaScript into a visual representation on the screen.
### Pipeline
1. Document Object Model Construction
	1. the browser receives the HTML document and begins parsing it to create the DOM, a tree structure that represents the document's content and structure.
	2. this process involves converting bytes to characters, identifying tokens, and building nodes incrementally as HTML is received.
2. CSS Object Model (CSSOM) Construction
	1. after constructing the DOM, the browser processes CSS files to create the CSSOM.
	2. this model represents the styles associated with the element with the element in the DOM, allowing the browser to understand how to style the content.
3. Render Tree Creation
	1. browser combines the DOM and CSSDOM to create the Render Tree. This tree includes only the nodes that need to be rendered on the screen, omitting any elements that are not visible (like those with `display: none`) and applying styles from the CSSOM.


---

## Related

[[Rendering performance]]
